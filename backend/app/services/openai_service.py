from openai import AsyncOpenAI
from openai import APIError, RateLimitError, APIConnectionError, APIStatusError
from typing import Optional, List
import asyncio
import tiktoken
from app.core.config import settings
from app.core.exceptions import DocumentProcessingError


class OpenAIService:
    """Service for interacting with OpenAI API to generate summaries."""
    
    def __init__(self):
        if not settings.openai_api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set")
        
        self.client = AsyncOpenAI(api_key=settings.openai_api_key)
        self.model = settings.openai_model
        
        try:
            self.encoding = tiktoken.encoding_for_model(self.model)
        except KeyError:
            self.encoding = tiktoken.get_encoding("cl100k_base")
        
        self.chunk_size_tokens = 10000
        self.chunk_overlap_tokens = 500
    
    def _count_tokens(self, text: str) -> int:
        """
        Count tokens in text using tiktoken.
        
        Args:
            text: Text to count tokens for
            
        Returns:
            Number of tokens
        """
        return len(self.encoding.encode(text))
    
    def _split_text_into_chunks(self, text: str) -> List[str]:
        """
        Split text into chunks based on token count with overlap for context preservation.
        Tries to break at sentence boundaries when possible.
        
        Args:
            text: Text to split
            
        Returns:
            List of text chunks
        """
        # Check if text fits in one chunk
        total_tokens = self._count_tokens(text)
        if total_tokens <= self.chunk_size_tokens:
            return [text]
        
        chunks = []
        # Split by sentences first for better chunking
        sentences = []
        current_sentence = ""
        
        for char in text:
            current_sentence += char
            if char in '.!?' and (len(current_sentence) == 1 or current_sentence[-2] != char):
                # Check if followed by space or newline
                if len(text) > len(current_sentence) and text[len(current_sentence)] in ' \n':
                    sentences.append(current_sentence.strip())
                    current_sentence = ""
        
        if current_sentence.strip():
            sentences.append(current_sentence.strip())
        
        # Combine sentences into chunks based on token count
        current_chunk = []
        current_tokens = 0
        
        for sentence in sentences:
            sentence_tokens = self._count_tokens(sentence)
            
            if sentence_tokens > self.chunk_size_tokens:
                if current_chunk:
                    chunks.append(' '.join(current_chunk))
                    current_chunk = []
                    current_tokens = 0
                chunks.append(sentence)
                continue
            
            if current_tokens + sentence_tokens > self.chunk_size_tokens and current_chunk:
                chunks.append(' '.join(current_chunk))
                # Start new chunk with overlap (last few sentences) for context preservation
                overlap_sentences = []
                overlap_tokens = 0
                for s in reversed(current_chunk):
                    s_tokens = self._count_tokens(s)
                    if overlap_tokens + s_tokens <= self.chunk_overlap_tokens:
                        overlap_sentences.insert(0, s)
                        overlap_tokens += s_tokens
                    else:
                        break
                current_chunk = overlap_sentences + [sentence]
                current_tokens = overlap_tokens + sentence_tokens
            else:
                current_chunk.append(sentence)
                current_tokens += sentence_tokens
        
        if current_chunk:
            chunks.append(' '.join(current_chunk))
        
        return chunks if chunks else [text]
    
    async def _generate_chunk_summary(self, text: str, chunk_num: int, total_chunks: int) -> str:
        """
        Generate summary for a single chunk.
        
        Args:
            text: Chunk text to summarize
            chunk_num: Current chunk number
            total_chunks: Total number of chunks
            
        Returns:
            Summary of the chunk
        """
        context = f" (Part {chunk_num} of {total_chunks})" if total_chunks > 1 else ""
        
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that creates concise, informative summaries of document sections. Focus on key points, main ideas, and important details."
                },
                {
                    "role": "user",
                    "content": f"Please provide a clear and structured summary of this document section{context}. Focus on the most important information:\n\n{text}"
                }
            ],
            temperature=0.7,
            max_tokens=2000
        )
        
        return response.choices[0].message.content.strip()
    
    async def generate_summary(self, text: str, max_length: int = None) -> str:
        """
        Generate a summary of the provided text using OpenAI API.
        For large documents, uses chunking strategy to save tokens.
        
        Args:
            text: The text content to summarize
            max_length: Maximum length of the summary in characters (optional)
        
        Returns:
            Generated summary string
        """
        # Split into chunks if document is large
        chunks = self._split_text_into_chunks(text)
        
        try:
            if len(chunks) == 1:
                # Small document - single API call
                response = await self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a helpful assistant that creates concise, informative summaries of documents. Focus on key points, main ideas, and important details."
                        },
                        {
                            "role": "user",
                            "content": f"Please provide a comprehensive summary of the following document. Make it clear, well-structured, and highlight the most important information:\n\n{text}"
                        }
                    ],
                    temperature=0.7,
                    max_tokens=4000
                )
                summary = response.choices[0].message.content.strip()
            else:
                # Large document - chunking strategy
                # Step 1: Summarize each chunk
                chunk_summaries = []
                for i, chunk in enumerate(chunks, 1):
                    chunk_summaries.append(await self._generate_chunk_summary(chunk, i, len(chunks)))
                    # Small delay to avoid rate limits
                    if i < len(chunks):
                        await asyncio.sleep(0.1)
                
                # Step 2: Combine chunk summaries into final summary
                combined_summaries = "\n\n".join([
                    f"Section {i+1} Summary:\n{summary}"
                    for i, summary in enumerate(chunk_summaries)
                ])
                
                response = await self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a helpful assistant that creates a comprehensive, unified summary from multiple document section summaries. Combine them into a coherent, well-structured final summary."
                        },
                        {
                            "role": "user",
                            "content": f"Please create a comprehensive final summary from these document section summaries. Make it clear, well-structured, and highlight the most important information from all sections:\n\n{combined_summaries}"
                        }
                    ],
                    temperature=0.7,
                    max_tokens=4000
                )
                summary = response.choices[0].message.content.strip()
            
            # Ensure summary doesn't exceed max_length if specified
            if max_length and len(summary) > max_length:
                summary = summary[:max_length] + "..."
            
            return summary
            
        except RateLimitError as e:
            raise DocumentProcessingError(
                f"OpenAI API rate limit exceeded. Please try again later. Details: {str(e)}"
            )
        except APIConnectionError as e:
            raise DocumentProcessingError(
                f"Failed to connect to OpenAI API. Please check your internet connection. Details: {str(e)}"
            )
        except APIStatusError as e:
            status_code = getattr(e.response, 'status_code', None) if hasattr(e, 'response') else None
            if status_code == 401:
                raise DocumentProcessingError("Invalid OpenAI API key. Please check your OPENAI_API_KEY.")
            elif status_code == 403:
                raise DocumentProcessingError("OpenAI API access forbidden. Please check your API key permissions.")
            elif status_code == 429:
                raise DocumentProcessingError(
                    f"OpenAI API rate limit exceeded. Please try again later. Details: {str(e)}"
                )
            else:
                raise DocumentProcessingError(
                    f"OpenAI API error (status {status_code}): {str(e)}"
                )
        except APIError as e:
            raise DocumentProcessingError(f"OpenAI API error: {str(e)}")
        except Exception as e:
            raise DocumentProcessingError(f"Unexpected error generating summary: {str(e)}")
