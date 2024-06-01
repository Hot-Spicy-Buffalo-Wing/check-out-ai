# %%
import urllib.request
from PIL import Image
# %%
url="https://oaidalleapiprodscus.blob.core.windows.net/private/org-eTN9wj08xBAZcR34rTYe0emj/user-3muPcUV1yGWIqE0eIRHNYsqO/img-1Czwmc97WWgZLVuBOfnkTClD.png?st=2024-06-01T13%3A01%3A18Z&se=2024-06-01T15%3A01%3A18Z&sp=r&sv=2023-11-03&sr=b&rscd=inline&rsct=image/png&skoid=6aaadede-4fb3-4698-a8f6-684d7786b067&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2024-05-31T23%3A40%3A08Z&ske=2024-06-01T23%3A40%3A08Z&sks=b&skv=2023-11-03&sig=VRhd%2B0QBXgM%2BnuOwjbFtYJh4PZBWTqg3b0NcH6cnJBs%3D"
urllib.request.urlretrieve(url, "images/img3.png")
# %%
img=Image.open("images/img3.png")
img
# %%
