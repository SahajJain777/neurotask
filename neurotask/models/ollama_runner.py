# models/ollama_runner.py
import subprocess

def run_llm(prompt: str) -> str:
    """
    Uses the local Gemma 3 model (via Ollama) to generate output for a given prompt.
    
    Args:
        prompt (str): The prompt text to be processed by the LLM.
    
    Returns:
        str: The generated response from Gemma 3, or an empty string if an error occurs.
    """
    try:
        # Start the subprocess to run the command
        process = subprocess.Popen(
            ["ollama", "run", "gemma3:4b", prompt],  # Pass prompt directly as argument
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Increased timeout to 300 seconds (5 minutes)
        stdout, stderr = process.communicate(timeout=300)
        
        # Check if the process exited with an error
        if process.returncode != 0:
            print(f"[LLM Error] Ollama returned error: {stderr}")
            return ""
        
        # Clean and return the response
        response = stdout.strip()
        if not response:
            print("[LLM Warning] Empty response received from model")
            return ""
            
        return response
    
    except subprocess.TimeoutExpired as te:
        print(f"[LLM Timeout] The process timed out after 5 minutes: {te}")
        process.kill()  # Ensure the process is terminated
        return ""
    except Exception as e:
        print(f"[LLM Exception] An error occurred while running the LLM: {e}")
        return ""

# Example usage:
if __name__ == "__main__":
    test_prompt = "Summarize the following text in one sentence:\nNeurotask is designed to organize files based on AI analysis."
    response = run_llm(test_prompt)
    print("Generated Response:", response)