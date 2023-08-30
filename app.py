import streamlit as st
from collections import Counter
from wordcloud import WordCloud
from streamlit_extras.colored_header import colored_header

from streamlit_extras.toggle_switch import st_toggle_switch
from streamlit_extras.stoggle import stoggle
from PIL import Image, ImageDraw, ImageFont
import io
import numpy as np
import random
from linkedin_api import Linkedin
def convertToPNG(image):
    # Convert PIL image to byte array
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='PNG')
    return img_byte_arr.getvalue()

api = Linkedin(st.secrets['name'], st.secrets['password'])
def getID(url):
    try:
        return url.split('/in/')[1].split('/')[0]
    except:
        return False
@st.cache
def getInfo(id):
    global api
    profile = api.get_profile(id)
    skills = [x['name'] for x in api.get_profile_skills(id)]
    summery = profile['summary']
    name = profile['firstName'] + ' ' + profile['lastName']
    honors = [x['title'] for x in profile['honors']]
    education = [x['schoolName'] for x in profile['education']]
    titles = [x['title'] for x in profile['experience']]
    companies = [x['companyName'] for x in profile['experience']]

    return name,skills, summery,  honors,education, titles, companies

def introduceRandomness(range):
    return random.randrange(range[0],range[1])/100
def genarateDict(info, nameMultiplier = 0 ,skillsMultiplier = 2, honorsMultiplier = 3, educationMultiplier = 3, titlesMultiplier = 4, companiesMultiplier = 1):
    name,skills, summery,  honors,education, titles, companies = info
    dic = {}
    for i in skills:
        dic[i] = skillsMultiplier * introduceRandomness([70,100])
    for i in honors:
        dic[i] = honorsMultiplier * introduceRandomness([70,100])
    for i in education:
        dic[i] = educationMultiplier * introduceRandomness([70,100])
    for i in titles:
        dic[i] = titlesMultiplier * introduceRandomness([70,100])
    for i in companies:
        dic[i] = companiesMultiplier * introduceRandomness([70,100])
    dic[name] = nameMultiplier * introduceRandomness([70,100])

    return dic



themes = {
    "Newspaper": {
        "background_color": "white",
        "colormap": "binary",
        "contour_color": "gray",
    },
    "orange attack": {
        "background_color": "coral",
        "colormap": "inferno",
        "contour_color": "#FFB72E",
    },
    "sky": {
        "background_color": "skyblue",
        "colormap": "viridis",
        "contour_color": "teal",
    },
    "Oceanic": {
        "background_color": "teal",
        "colormap": "ocean",
        "contour_color": "#FFFFFF",
    },
    "Earthy": {
        "background_color": "tan",
        "colormap": "terrain",
        "contour_color": "#DB682C",
    },
    "Winter Wonderland": {
        "background_color": "white",
        "colormap": "winter",
        "contour_color": "purple",
    },
    "Volcano": {
        "background_color": "orangered",
        "colormap": "YlOrRd",
        "contour_color": "#FFBB26",
    },
    "ash": {
        "background_color": "black",
        "colormap": "cividis",
        "contour_color": "gray",
    },
    "spring": {
        "background_color": "teal",
        "colormap": "Spectral",
        "contour_color": "#EDFFC1",
    },
    'blueOnWhite':{
        'background_color':'white',
        'colormap': 'Blues',
        'contour_color': 'black',

    },
    'redOnWhite':{
        'background_color':'white',
        'colormap': 'Reds',
        'contour_color': 'black',
    },
    'greenOnWhite':{
        'background_color':'white',
        'colormap': 'Greens',
        'contour_color': 'black',
    },
    'whiteOnBlack':{
        'background_color':'black',
        'colormap': 'Greys',
        'contour_color': 'white',
    },
    'greenOnBlack':{
        'background_color':'black',
        'colormap': 'Greens',
        'contour_color': 'white',
    },
    'redOnBlack':{
        'background_color':'black',
        'colormap': 'Reds',
        'contour_color': 'white',
    },
    'blueOnBlack':{
        'background_color':'black',
        'colormap': 'Blues',
        'contour_color': 'white',
    },
    'yellowOnBlack':{
        'background_color':'black',
        'colormap': 'YlOrBr',
        'contour_color': 'white',
    },
    'orangeOnBlack':{
        'background_color':'black',
        'colormap': 'Oranges',
        'contour_color': 'white',
    },
    'purpleOnBlack':{
        'background_color':'black',
        'colormap': 'Purples',
        'contour_color': 'white',
    },
    'pinkOnBlack':{
        'background_color':'black',
        'colormap': 'pink',
        'contour_color': 'white',
    },
    'whiteOnBlue':{
        'background_color':'blue',
        'colormap': 'Greys',
        'contour_color': 'white',
    },
    'whiteOnRed':{
        'background_color':'red',
        'colormap': 'Greys',
        'contour_color': 'white',
    },
    'whiteOnGreen':{
        'background_color':'green',
        'colormap': 'Greys',
        'contour_color': 'white',
    }
    
}


@st.cache(allow_output_mutation=True)
def getBanners():
    return []

@st.cache(allow_output_mutation=True)
def getPNGs():
    return []



colored_header("Linkedin word cloud", color_name="violet-70",     description="make your linkedin pop",)

st.write("This is a word cloud generator for your linkedin profile. It will generate a word cloud based on the words you use the most in your profile. It will also generate a word cloud based on the words you use the most in your job descriptions.")
button_pressed = False
## get the linkedin profile url
url = ''

banners = getBanners()
pngs = getPNGs()
@st.cache
def prepare_mask(name):
    def draw_text(image, text, font_path, size, color, padding_left=0, padding_right=0, padding_top=0, padding_bottom=0):
        font = ImageFont.truetype(font_path, size)
        draw = ImageDraw.Draw(image)

        max_text_width = image.size[0] - (padding_left + padding_right)
        max_text_height = image.size[1] - (padding_top + padding_bottom)

        while font.getsize(text)[0] > max_text_width or font.getsize(text)[1] > max_text_height:
            size -= 1
            font = ImageFont.truetype(font_path, size)
        
        text_width, text_height = font.getsize(text)
        
        x_position = padding_left
        y_position = (image.size[1] - text_height - padding_top - padding_bottom) / 2 + padding_top

        draw.text((x_position, y_position), text, fill=color, font=font)
    image = Image.new('RGB', (1584, 396), color=(0, 0, 0))
    text = name
    draw_text(image, text, "./Roboto-bold.ttf", 300 , "white", padding_right=100, padding_top=150, padding_left=600)
    return np.array(image)

url = st.text_input("Enter your linkedin profile url")
id = getID(url)
if not id:
    st.write("please enter a valid linkedin url")
    st.stop()
info = getInfo(id)





# Print the words and their frequencies
# for word, frequency in word_frequencies.items():

#     st.write(f'{word}: {frequency}')

# Define a state variable to store the list of words
theme = st.selectbox("color theme", themes.keys())
col1, col2 = st.columns(2)
with col1:
    include_name = st_toggle_switch(
        label="Include name in word cloud",
        key="switch_1",
        default_value=True,
        label_after=True,
        inactive_color="#D3D3D3",  # optional
        active_color="#11567f",  # optional
        track_color="#29B5E8",  # optional
    )
with col2:
    advanced_options = st_toggle_switch(
        label="advanced options",
        key="switch_2",
        default_value=False,
        label_after=True,
        inactive_color="#D3D3D3",  # optional
        active_color="#11567f",  # optional
        track_color="#29B5E8",  # optional
    )

mask = prepare_mask(info[0] if include_name else '')


skillMultiplier = 2
honorsMultiplier = 3
educationMultiplier = 3
titlesMultiplier = 4
companiesMultiplier = 1
nameMultiplier = 0

if advanced_options:
    """
    ###### choose the size of words or phrases in each category:
    """
    skillMultiplier = st.slider("size of skills", 0, 4, 2)
    honorsMultiplier = st.slider("size of honors", 0, 4, 3)
    educationMultiplier = st.slider("size of education", 0, 4, 3)
    titlesMultiplier = st.slider("size of job titles", 0, 4, 4)
    companiesMultiplier = st.slider("size of companies names", 0, 4, 1)
    nameMultiplier = 0


if st.button("generate linkedin banner"):
    dic = genarateDict(info, nameMultiplier, skillMultiplier, honorsMultiplier, educationMultiplier, titlesMultiplier, companiesMultiplier)
    banners.append( WordCloud(background_color = themes[theme]['background_color'],  contour_width = 5, min_font_size=20,
        contour_color = themes[theme]['contour_color'], colormap = themes[theme]['colormap'], width = 1584, height = 396, mask=mask).generate_from_frequencies(dic).to_image())#txt
    pngs.append(convertToPNG(banners[-1]))




# st.sidebar.toggle()

    # Convert byte array to bytes


for banner in range(len(banners),0,-1):
    st.image(banners[banner-1])
    st.download_button("download banner", pngs[banner -1], "linkedin_banner.png", "image/png")
if len (banners) > 0:
    if st.button("clear banners"):
        banners.clear()
        pngs.clear()
        st.experimental_rerun()