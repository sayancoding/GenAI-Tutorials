import os
import shutil
import tempfile
from git import Repo 

def clone_repo_to_local(repo_url: str):

    local_dir = tempfile.mkdtemp(prefix="agent_docs_")
    print(f"Cloning {repo_url} into {local_dir}...")
    
    try:
        # Perform the clone
        # depth=1 performs a 'shallow clone' which is much faster 
        # because it only pulls the latest code, not the whole history.
        Repo.clone_from(repo_url, local_dir, depth=1)
        print("Clone successful!")
        return local_dir
        
    except Exception as e:
        print(f"Error cloning repository: {e}")
        # Cleanup if it fails
        if os.path.exists(local_dir):
            shutil.rmtree(local_dir)
        return None


def build_repo_context(repo_path):
    context = "ACT AS A SENIOR ARCHITECT. ANALYZE THIS REPO:\n\n"
    
    for root, dirs, files in os.walk(repo_path):
        # Skip hidden/junk folders
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', 'venv']]
        
        for file in files:
            if file.endswith(('.py', '.js', ".ts" '.java' , ".html", '.md', '.txt')): 
                full_path = os.path.join(root, file)
                relative_path = os.path.relpath(full_path, repo_path)
                
                with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    # Wrapping in tags for the Agent
                    context += f"\n<file path='{relative_path}'>\n{content}\n</file>\n"
    
    return context