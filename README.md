# PostGird 

A blog application with [django](https://djangoprojects.com) and [nanodjango]()

## Get Started 🎯
- Create a virtual environment 📁
```bash
#using uv
uv venv venv
# venv
python -m venv venv
```
- Install the dependencies 🛠
```bash
# using uv 
uv run pip install -r requirements.txt
```
- Setting `env.`  ⚙
```python
DJANGO_SECRET_KEY=""
DJANGO_DEBUG=True
```
 ### Working dir 📂
 ```
 cd src/
 ```
 ### Migrate 🚴‍♂️
 ```bash
 uv run nanodjango run app.py
 ```
 ### Runserver 🚀
```bash
uv run nanodjango manage app.py runserver
```

### Clone the repository 📌

```bash
git clone https://github.com/RaphaelApeh/blog.git
```
