from langchain.utilities import SerpAPIWrapper
import os


os.environ["SERPAPI_API_KEY"] = '31a3c96f0ce535fd1b43117d3c9298c66753b6dae1da9074708f03ecc8282367'
search = SerpAPIWrapper()
result = search.run("松江大学城中的上海工程技术大学的所有建筑物？")
print(result)
