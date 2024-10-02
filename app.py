from io import BytesIO

import requests
import streamlit as st
from PIL import Image

from agents.blog_assistant import BlogAssistant
from agents.user_proxy_agent import UserProxyAgent
from agents.vision_assistant import VisionAssistant
from config import Config
from constants import MAX_CHAT_ROUNDS
from utils.agent_manager import AgentManager


def main():
    st.title("Travel Blog Writer App")

    image_url = st.text_input("Enter the Image URL of the Travel Destination")

    if image_url:
        try:
            response = requests.get(image_url)
            image = Image.open(BytesIO(response.content))
            if image.format.lower() not in ["jpeg", "png", "ppm", "gif", "tiff", "bmp"]:
                st.error(
                    f"Unsupported image format: {image.format}. Please use JPEG, PNG, PPM, GIF, TIFF, or BMP."
                )
            else:
                # Display the image in a 224x224 container
                st.image(image, caption="Travel Destination", width=224)
        except requests.exceptions.RequestException:
            st.error("Failed to fetch the image. Please check the URL and try again.")
        except Exception as e:
            st.error(f"An error occurred: {e}")

    if st.button("Generate Blog Post"):
        if not image_url:
            st.warning("Please enter an image URL.")
        else:
            with st.spinner("Generating blog post..."):
                try:
                    # Validate image URL and format
                    response = requests.get(image_url)
                    image = Image.open(BytesIO(response.content))
                    if image.format.lower() not in [
                        "jpeg",
                        "png",
                        "ppm",
                        "gif",
                        "tiff",
                        "bmp",
                    ]:
                        st.error(
                            f"Unsupported image format: {image.format}. Please use JPEG, PNG, PPM, GIF, TIFF, or BMP."
                        )
                        st.stop()

                    user_proxy = UserProxyAgent()
                    vision_assistant = VisionAssistant()
                    blog_assistant = BlogAssistant()
                    manager = AgentManager(
                        user_proxy=user_proxy,
                        vision_assistant=vision_assistant,
                        blog_assistant=blog_assistant,
                    )

                    result = manager.run(image_url)
                    st.success("Blog post generated successfully!")

                    # Extract and display only the blog text in markdown format
                    if hasattr(result, "summary"):
                        blog_text = result.summary
                    else:
                        blog_text = str(result)

                    st.markdown(blog_text)
                except requests.exceptions.RequestException:
                    st.error(
                        "Failed to fetch the image. Please check the URL and try again."
                    )
                except Exception as e:
                    st.error(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
