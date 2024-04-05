## Setting Up "shop-intel" Repository


1. **Clone the Repository:**
   ```bash\n   git clone git@github.com:arkamaldeen/shop-intel.git```

2. **Navigate to the Repository Directory:**
   ```bash\n   cd shop-intel\n   ```

3. **Create a Virtual Environment:**
   ```bash\n   python -m venv .venv\n   ```

4. **Activate the Virtual Environment:**
   ```bash\n   .venv\\scripts\\activate\n   ```

5. **Install Dependencies in the Virtual Environment:**
   ```bash\n   pip install -r requirements.txt\n   ```

6. **Install Docker and Run Docker Desktop:**
   ```bash\n   docker pull qdrant/qdrant\n   ```

7. **Run Qdrant Docker:**
   ```bash\n   docker run -p 6333:6333 -v .:/qdrant/storage qdrant/qdrant\n   ```

8. **Run Python File:**
   ```bash\n   python app.py\n   ```


This set of instructions guides you through setting up and running the "shop-intel" repository, including cloning the repository, setting up a virtual environment, installing dependencies, running Docker, and executing the Python file.
