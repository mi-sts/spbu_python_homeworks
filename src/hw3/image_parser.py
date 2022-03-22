import asyncio
from bs4 import BeautifulSoup
import os
import aiohttp
import sys

DIRECTORY_NAME = "parsed_images"
URL = "https://www.thisfuckeduphomerdoesnotexist.com"


async def parse_image(session: aiohttp.ClientSession) -> None:
    async with session.get(URL) as response:
        if response.status != 200:
            print("Request status is not successful!")
            return
        soup = BeautifulSoup(await response.read(), "html.parser")
        image_link = soup.find("img", id="image-payload").get("src")
        async with session.get(image_link) as image_response:
            if image_response.status != 200:
                print("Image request is not successful!")
                return
            image_content = await image_response.content.read()
            image_name = image_link.split("/")[-1]
            with open(f"{DIRECTORY_NAME}/image_{image_name}.jpg", "wb") as image_file:
                image_file.write(image_content)


def _create_directory() -> bool:
    if not os.path.exists(DIRECTORY_NAME):
        try:
            os.makedirs(DIRECTORY_NAME)
        except OSError:
            print("Can't create the images directory!")
            return False

    return True


def _get_number_argument() -> object:
    if len(sys.argv[1:]) != 1:
        print("Wrong number of arguments!")
        return None
    try:
        image_number = int(sys.argv[1])
    except ValueError:
        print("Wrong argument type!")
        return None

    return image_number


async def main() -> None:
    image_number = _get_number_argument()
    if image_number is None:
        return
    if not _create_directory():
        return

    async with aiohttp.ClientSession() as session:
        await asyncio.gather(*[parse_image(session) for _ in range(image_number)])


if __name__ == "__main__":
    asyncio.run(main())
