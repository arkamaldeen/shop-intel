## Setting Up "shop-intel" Repository


1. **Clone the Repository:**
```
git clone git@github.com:arkamaldeen/shop-intel.git
```

2. **Navigate to the Repository Directory:**
```
cd shop-intel
```

3. **Create a Virtual Environment:**
```
python -m venv .venv
```

4. **Activate the Virtual Environment:**
 ```
   .venv\scripts\activate
 ```

5. **Install Dependencies in the Virtual Environment:**
```
pip install -r requirements.txt
```

6. **Install Docker and Run Docker Desktop:**
```
docker pull qdrant/qdrant
```

7. **Run Qdrant Docker:**
```
docker run -p 6333:6333 -v .:/qdrant/storage qdrant/qdrant
```

8. **Run Python File:**
```
python app.py
```


This set of instructions guides you through setting up and running the "shop-intel" repository, including cloning the repository, setting up a virtual environment, installing dependencies, running Docker, and executing the Python file.
