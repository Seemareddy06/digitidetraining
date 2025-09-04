import streamlit as st
import boto3
import json

# AWS Bedrock Client 
client = boto3.client(
    service_name="bedrock-runtime",
    region_name="ap-south-1", 
    aws_access_key_id="AKIAUYLSMZO2EXG4MGLG",      
    aws_secret_access_key="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"   
)

# Model ID for LLaMA 3 (8B Instruct version)
MODEL_ID = "meta.llama3-8b-instruct-v1:0"
#  Streamlit UI 
st.title("Amazon_bedrock clone")
st.write(f"Using Model ID: `{MODEL_ID}`")

prompt = st.text_area("Enter your prompt:", "Give me 3 easy dinner ideas.")

if st.button("Generate Response"):
    if prompt.strip():
        with st.spinner("Generating response..."):
            try:
                body = json.dumps({
                    "prompt": prompt,
                    "max_gen_len": 512,
                    "temperature": 0.7,
                    "top_p": 0.9
                })

                response = client.invoke_model(
                    modelId=MODEL_ID,
                    body=body,
                    contentType="application/json",
                    accept="application/json"
                )

                result = json.loads(response["body"].read())
                output = result.get("generation", "No output found")

                st.subheader("🍽️ AI Response:")
                st.write(output)

            except Exception as e:
                st.error(f"Error generating response: {e}")
    else:
        st.warning("Please enter a prompt.")
