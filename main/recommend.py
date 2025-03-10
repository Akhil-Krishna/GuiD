





# import sys
# import os

# # Add the path to RecommendationEngine   C:\Users\akhil\RecommendationEngine\predictor.py
# recommendation_engine_path = r"C:\Users\akhil\RecommendationEngine"

# # Add it to sys.path
# sys.path.append(recommendation_engine_path)

# # Now import the function from predictor.py
# from predictor import predict
# # In recommend.py
# from RecommendationEngine.predictor import predict

# # In recommend.py
# from ....RecommendationEngine.predictor import predict

# # In recommend.py
# import sys
# sys.path.append("C:\\Users\\akhil")
# from RecommendationEngine.predictor import predict


courses={
    "Semester1":['Think To Code'],
    "Semester2":['Python Basics'],
    "Semester3":['Stack',"Queue","LinkedList"],
    'Semester4':['Database'],
    'Semester5':['Dynamic Programming'],
    'Semester6':['Graph,Tree'],
    'Semester7':["Analysing Code"],
    'Semester8':['Interview Preparation']
}

# def recommender(inp=[33,100,2,32,100,2,46,67,3,36,102,1,35,60,3,36,110,1,25,50,6,45,102,2]):
#     result=predict(inp)
#     return courses[result]

# print(recommender())
    
import subprocess
import json

def call_predict_function(input_data=[25,100,2,32,100,2,46,67,3,36,102,1,35,60,3,36,110,1,25,50,6,45,102,2]):
    # Convert your input data to JSON
    input_json = json.dumps(input_data)
    
    # Full path to Python 3.9 executable - MODIFY THIS PATH to match your system
    python_path = r"C:\Users\akhil\AppData\Local\Programs\Python\Python39\python.exe"  # or wherever your Python 3.9 is installed
    
    # Call the predict script with the compatible Python version
    result = subprocess.run(
        [python_path, "C:/Users/akhil/RecommendationEngine/predictor_wrapper.py", input_json],
        capture_output=True,
        text=True,
        encoding='utf-8'  # Specify UTF-8 encoding
    )
   
    # Parse the result
    if result.returncode != 0:
        print("Error:", result.stderr)
        return None
    
    try:
        # Print raw output for debugging
        #print("Raw output:", result.stdout)
        res=result.stdout.strip().split('\n')[-1].split('"')[1]
        return res
    except:
        print("Failed to parse JSON response:", result.stdout)
        return None


# Example usage
if __name__ == "__main__":
    # Replace this with your actual input data
    sample_data = [43,100,2,47,100,2,46,67,3,46,102,1,45,60,3,50,110,1,25,50,6,45,102,2]
    
    # Call the prediction function
    predictions = call_predict_function(sample_data)
    
    if predictions:
        print("Received predictions:", predictions)