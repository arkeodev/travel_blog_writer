import base64  # Add this import
import json  # Add this import
from io import BytesIO

import requests  # Add this import
import streamlit as st
from PIL import Image

from agents.blog_assistant import BlogAssistant
from agents.user_proxy_agent import UserProxyAgent
from agents.vision_assistant import VisionAssistant
from config import Config
from models.travel_destination import TravelDestination  # Add this import
from utils.agent_manager import AgentManager
from utils.file_utils import save_uploaded_file
from utils.image_utils import USER_AGENT, fetch_image, resize_image


def main():
    st.set_page_config(layout="wide")
    st.title("Travel Blog Writer App")

    # Add explanation about the app
    st.markdown(
        """
    ## Welcome to the Travel Blog Writer App!

    This application uses advanced AI to generate travel blog posts based on images of destinations. Here's how it works:

    1. Enter your Fireworks AI API key in the sidebar.
    2. Choose whether to upload a local image file or enter an image URL.
    3. Upload your image or paste the URL of an image showing a travel destination.
    4. Click the "Generate Blog Post" button.
    5. The app will analyze the image and create a unique blog post about the location.

    The process involves:
    - A Vision Assistant that interprets the image.
    - A Blog Assistant that crafts the content.
    - A User Proxy that manages the interaction between these AI agents.

    Enjoy your AI-generated travel blogs!
    """
    )

    # Add sidebar for API key input
    st.sidebar.title("Configuration")
    api_key = st.sidebar.text_input("Enter Fireworks AI API Key", type="password")

    # Update Config with the entered API key
    if api_key:
        Config.FIREWORKS_API_KEY = api_key

    # Add option to choose between local file and URL
    image_source = st.radio("Choose image source:", ("Upload local file", "Enter URL"))

    image = None
    normalized_image = None
    if image_source == "Upload local file":
        uploaded_file = st.file_uploader(
            "Choose an image file", type=["jpg", "jpeg", "png", "gif", "tiff", "bmp"]
        )
        if uploaded_file is not None:
            # Save the uploaded file and get the file path
            file_path = save_uploaded_file(uploaded_file)
            image = Image.open(file_path)
            # Normalize the image
            with open(file_path, "rb") as image_file:
                normalized_image = resize_image(image_file)
    else:
        image_url = st.text_input("Enter the Image URL of the Travel Destination")
        if image_url:
            try:
                image = fetch_image(image_url)
                # Normalize the image
                normalized_image = resize_image(
                    BytesIO(
                        requests.get(
                            image_url, headers={"User-Agent": USER_AGENT}
                        ).content
                    )
                )
            except requests.exceptions.RequestException as e:
                st.error(f"Failed to fetch the image: {e}")
            except Exception as e:
                st.error(f"An error occurred while processing the image: {e}")

    if image is not None:
        # Display the original image in a 224x224 container
        st.image(image, caption="Travel Destination", width=224)
    else:
        st.warning("No valid image has been uploaded or fetched.")

    if st.button("Generate Blog Post"):
        if not api_key:
            st.warning("Please enter your Fireworks AI API Key in the sidebar.")
        elif normalized_image is None:
            st.warning("Please upload an image or enter a valid image URL.")
        else:
            with st.spinner("Generating blog post..."):
                try:
                    user_proxy = UserProxyAgent()
                    vision_assistant = VisionAssistant()
                    blog_assistant = BlogAssistant()
                    manager = AgentManager(
                        user_proxy=user_proxy,
                        vision_assistant=vision_assistant,
                        blog_assistant=blog_assistant,
                    )

                    result = manager.run(normalized_image)

                    # Extract the content from the vision_assistant's response
                    vision_assistant_response = None
                    for message in result:
                        if message["speaker"] == "vision_assistant":
                            vision_assistant_response = message["content"]
                            break

                    if vision_assistant_response:
                        # Parse the JSON string to a dictionary
                        travel_data = json.loads(vision_assistant_response)

                        # Create TravelDestination instance
                        travel_destination = TravelDestination(**travel_data)

                        if (
                            travel_destination.confidence_score < 0.7
                        ):  # You can adjust this threshold
                            st.warning(
                                f"Low confidence in destination identification (score: {travel_destination.confidence_score}). Please try a different image."
                            )
                        else:
                            st.success("Blog post generated successfully!")
                            st.markdown(f"# {travel_destination.destination_name}")
                            st.markdown(travel_destination.description)

                            if travel_destination.attractions:
                                st.markdown("## Attractions")
                                for attraction in travel_destination.attractions:
                                    st.markdown(f"- {attraction}")

                            # Add similar sections for transportation, accommodation, and restaurants if needed

                except Exception as e:
                    st.error(f"An error occurred: {e}")
                    st.error(f"Result: {result}")  # Add this line for debugging


if __name__ == "__main__":
    main()
