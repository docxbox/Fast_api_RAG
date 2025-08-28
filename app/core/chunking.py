from typing import List
import re 

def fixed_chunk(text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
    """ 
     Split text into fixed size chunks


     args:
        text (str): The text to be chunked
        chunk_size (int): The size of each chunk
        overlap (int): The number of overlapping characters between chunks

    returns:
        List[str]: A list of text chunks
    """

    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start = end - overlap
        if start < 0:
            start = 0
    return chunks


def semantic_chunk(text: str, min_chunk_size: int = 200, max_chunk_size: int = 1000) -> List[str]:
    """ 
    Split text into semantically by paragraphs/sentences while keeping chunks between min and max size.

    args:
        text (str): text to be chunked
        min_chunk_size (int): The minimum size of each chunk
        max_chunk_size (int): The maximum size of each chunk

    returns:
        List[str]: list of semantically split text chunks.
    """

    paragraphs = re.split(r'\n+', text)
    chunks = []
    current_chunk = ""

    for paragraph in paragraphs:
        if len(current_chunk) + len(paragraph) + 1 <= max_chunk_size:
            if current_chunk:
                current_chunk += "\n" + paragraph
            else:
                current_chunk = paragraph
        else:
            if len(current_chunk) >= min_chunk_size:
                chunks.append(current_chunk)
                current_chunk = paragraph
            else:
                if current_chunk:
                    current_chunk += "\n" + paragraph
                else:
                    current_chunk = paragraph

            while len(current_chunk) > max_chunk_size:
                split_point = current_chunk.rfind('.', 0, max_chunk_size)
                if split_point == -1 or split_point < min_chunk_size:
                    split_point = max_chunk_size
                chunks.append(current_chunk[:split_point + 1].strip())
                current_chunk = current_chunk[split_point + 1:].strip()

    if current_chunk:
        chunks.append(current_chunk)

    return chunks


def chunk_text(text: str, strategy: str = "fixed", **kwargs) -> List[str]:
    """ 
    main interface for chunking text using different strategies.

    args:
        text (str): The text to be chunked
        strategy (str): The chunking strategy to use ("fixed" or "semantic")
        **kwargs: Additional arguments for the chunking function

    returns:
        List[str]: A list of text chunks
    """

    if strategy == "fixed":
        return fixed_chunk(text, **kwargs)
    elif strategy == "semantic":
        return semantic_chunk(text, **kwargs)
    else:
        raise ValueError("Invalid chunking strategy. Use 'fixed' or 'semantic'.")