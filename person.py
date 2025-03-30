import datetime
import streamlit as st
import pandas as pd 
import json
import os
import time
import random
import plotly.express as px 
import plotly.graph_objects as go 
from streamlit.lottie import st_lottie 
import requests


# set page config
st.set_page_config(
    page_title="Personal\library",
    page_icon="📚",
    layout= "wide",
    initial_sidebar_state="expanded"
)

# custom cs for stying
st.markdown("""
<style>
    .main-header{

        font-size: 3rem !important,
        color: #1E3A8A,
        font-weight: 700,
        margin-bottom: 1rem,
        text-align:center,
        text-shadow: 2px 2px 4px rgba(0,0,0,0,0.1),
    }
    .sub_header{
            font-size: 1.8rem!important,
            color:3B82F6,
            font-weight:600,
            margin-top:1rem,
            margin-botton:1rem,
    }
    .sucess-message{
            padding:1rem,
            bankgound-color:#ECFDF5,
            border-left: 5px solid #10B981,
            border-radius: 0.375rem
            
            }
            .warning-message {
            padding:1rem,
            background-color: #FE3C7,
            border-left:5px solid #F59E0B,
        }
        .book-card {
            background-color:#F3F4F6,
            border-radius: 0.5rem,
            padding:1rem,
            margin-botton:1rem,
            border-left: 5px solid #3B82F6,
            transtion: transfrom 0.3 ease,
        }
        .book-card-hover {
            transofrm: translatey(-5px)
            box-shadow:0 10px 15px -3px rgba(0,0,0,0,0.1),
        }
        .read-badge {
            background-color:#10B981,
            color:white,
            padding:0.25rem 0.75rem,
            border-radius: 1rem,
            font-size: 0.8rem,
            font-wegth: 600,
        }
        .unread-badge{
            background-color:#10B981,
            color:white,
            padding:0.25rem 0.75rem,
            border-radius: 1rem,
            font-size: 0.8rem,
            font-wegth: 600,

        }
        .action-button {
            margin-right:0.5rem,            
        }
        .stButton>button {
            border-radius:0.375rem,
        }
</style>
""",unsafe_allow_html=True)



def load_lottieurl(url):
    try:
        r =requests.get(url)
        if r.status_code != 200:
           return None
        return r.json()
    except:
        return None
    

if 'library' not in st.session_state:
    st.session_state.libary = []
if'search_results' not in st.session_state:
    st.session_state.search_result = []
if'book added' not in st.session_state:
    st.session_state.book_added = False
if'book removed' not in st.session_state:
    st.session_state.book_removed = False
if'current_view' not in st.session_state:
    st.session_state.current_view = 'library'

def load_library():
    try:
        if os.path.exists('library.json'):
            with open('library.json','r') as file:
                st.session_state.library = json.load(file)
                return True
            return False
    except Exception as e:
        st.error(f"Error loading library:{e}")
        return False

#save librar
def save_library():
    try:
        with open('library.json','w') as file:
            json.dump(st.session_state.library,file)
            return True
    except Exception as e:
         st.error(f"Error loading library:{e}")
         return False

# add a book to library
def add_book(title,autor,publication_year,genre,read_status):
    book ={
        'title': title,
        'autor': autor,
        'publication_year':publication_year,
        'genre' : genre,
        'read_status' : read_status,
        'added_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    st.session_state.library.append(book)
    save_library()
    st.session_state.book_added = True
    time.sleep(0.5)  #animation delay

#remove books 
def remove_book(index):
    if 0 <= index <len (st.session_state.library):

        del st.session_state.library[index]
        save_library()
        st.session_state.book_removed = True
        return True
    return False

# search books
def search_books(search_term,search_by):
    search_term = search_term.lower()
    results = []

    for book in st.session_state.library:
        if search_by=="Title"and search_term in book['title'].lower():
            results.append(book)
        elif search_by  == "Autor" and search_term in book['autor'].lower():
            results.append(book)
        elif search_by  == "Genre"and search_term in book['genre'].lower():
            results.append(book)
    st.session_state.search_results = results

# calculate library stats
def get_library_stats():
    total_books = len(st.session_stats.library)
    read_books =sum(1 for book  in st.session_state.library if book('read status'))
    percent_read = (read_books / total_books * 100) if total_books > 0 else 0

    genres = {}
    authors = {}
    decades = {}

    for book in st.session_state.library:
        if book['gence'] in genres:
             genres[book['gener']] +- 1
        else: 
            genres[book['genre']] =1
    
        
        #count author
    if book['authors'] in authors :
        genres[book['authors']] +- 1
    else: 
        genres[book['authors']] =1
        

        #count decades
        decades = (book['publication_year']//10) * 10
    if book['decades'] in decades :
        genres[book['decades']] +- 1
    else: 
        genres[book['decades']] = 1

        # sort by count
    genres = dict(sorted (genres.items(), key=lambda x: x[1], reverse=True))
    authors = dict(sorted (authors.items(), key=lambda x: x[1], reverse=True))
    decades = dict(sorted (decades.items(), key=lambda x: x[0]))



    return{
         'total_books' : total_books,
         'read_books' :read_books,
         'percent_read' : percent_read,
         'genres': genres,
         'authors' : authors,
         'decades' : decades,
         
    }

def create_vislation(stats):
    if stats['total_books'] > 0:
        fig_read_stats = go.figure(data=[go.Pie( 
            lablels=['Read', 'Unread'],
            values= [stats['read_books'],stats['total_books']- stats['read_books']],
            hole = 4,
            marker_colors =['#10B981', '#F87171']
        )])

        fig_read_stats.updata_layout(
            title_text="Read vs Unread Books",
            showlegend = True,
            hight = 400
        )
        st.plotly_chart(fig_read_stats , use_container_width= True)
        # bar char genres
        if stats ['generes']:
            genres_df = pd.DataFrame({
                'Genre': list(stats['genres'].keys()),
                'count': list(stats['genres'].values()),

            })
            fig_decades = px.line(
                genres_df,
                x='Genre',
                y= 'count',
                color='count',
                color_continous_scale = px.colors.sequentail.Blues
            )
            fig_decades.update_Layout(
                title_text ='Books by publication',
                xaxis_title = "Genres",
                yaxis_title ='Nubers of books',
                height = 400
            )
            st.plotly_chart(fig_decades, use_container_width= True)
        if stats['decade']:
            decades_df = pd.DataFrame({
                'Decate': [f"{decade}s" for decade in stats['decates'].keys()],
                 'count' : list(stats['decades'].values())
            })
            fig_decades = px.line(
                decades_df,
                x = "Decade",
                y ='Count',
                markers = True,
                line_sape= "spline"
            )
           
            st.plotly_chart(fig_decades, use_container_width = True)
            
            # load library
load_library()
st.sidebar.markdown("<h1 stylr='text-align: center;'> Navigation</h1>",unsafe_allow_html =True)
lottie_book = load_lottieurl("https://assests9.lottiefiles.com/temp/if20_akAfIn.json")
if lottie_book:
    with st.sidebar:
        st_lottie(lottie_book, height=200,key ="book_animation")

nav_option = st.sidebar.radio(
    "choose an option",
    ["View library","Add Books","search Books","Library staristics"])

if nav_option == "view library":
    st.session_state.current_view = 'library'
elif nav_option == "Add Books":
    st.session_state.current_view = "add"
elif nav_option == "session Books":
    st.session_state.current_view = "search"
elif nav_option == "library statistics":
    st.session_state.current_view = "stats",

st.markdow("<h1 class = 'main-header'>personal library Manger</h1>",unsafe_allow_html = True)
if st.session_state.current_view == "add":
    st.markdown("<h2 class ='sub-header'Add a new book</h2>",unsafe_allow_html = True)

    # adding books input from
    with st.form(key= 'add_book_from'):
        col1, col2 =st.columns(2)

        with col1:
            title = st.text_input("Booktitle", max_chars=100)
            author = st.text_input("Author",max_chars= 100)
            publication_year = st.number_input("Publication Year", min_value=1000, max_value=datetime.datetime.now().year, step=1, value=2023)
        with col2:
            genre = st.selectbox("Genre",[
                "Friction", "Non-friction","science","Technology","Fanstasy","Romance", "Poetry self-help","Art","Religion","History"
            ])
            read_status = st.radio("Read status",["Read","Unread"], horizontal= True)
            read_bool = read_status == "Read"
        submit_button = st.form_submit_button
        if submit_button and title and author :
            add_book(title, author, publication_year,genre,read_bool)

    if st.session_state.book_added:
            st.markdown("<div class 'sucess-message> Book added sucwessfully!</div>",unsafe_all_html = True)
            st.balloons()
            st.session_state.book_added = False
elif st.session_state.current_view == "library":
    st.markdown("<h2 class ='sub-header'> Your library</h2>",unsafe_allow_html = True)

    if not st.session_state.library:
        st.markdown("<div> class ='warning-message>' Your library is empty .Add some books to get started!</div>",unsafe_allow_html = True)

    else:
        cols = st.columns(2)
        for i ,book in enumerate(st.session_state.library):
            with cols[i % 2]:
                st.markdown(f"""<div class = 'book-card'>
                            <h3>{book['title']} </h3>
                            <p><strong> Author:<strong> {book['author']}</p>
                            <p><strong> publicaltion year:<strong> {book['publicaltion_year']}</p>
                            <p><strong> Genre:<strong> {book['genre']}</p>
                            <p><span class ='{"read-badge"if book["read_status"]else"unread-badge"}'>{
                                "Read" if book["read_status"] else "Unread"
                            }</span></p>
                            </div>                           
""",unsafe_allow_html =True)
                
                col1,col2 = st.column(2)
                with cols:
                    if st.button(f"Remove",key=f"remove_{i}",use_container_width = True):
                        if remove_book(i):
                           st.reurn()
                        with col2:
                            new_status = not book['read_stats']
                            status_label ="Mark as read" if not book['read_status'] else "Mark as Unread"
                            if st.button(status_label,key=f"status_{i}", use_container_width= True):
                                st.session_state.libraray[i]['read_status'] = new_status
                                save_library()
                                st.rerun()
    if st.session_state.book_removed:
        st.markdown("<div class='success-message'>Book removed suscessfully!")
        st.session_state.book_removed = False
elif st.session_state.current_view == "search":
    st.markdown("<h2 class='sub-header'> search books</h2> ",unsafe_allow_html=True)

    search_by = st.selectbox("search by:",["Title","Authon","Genre"])
    search_term =st.text_input("Enter search term:")

    if st.button("Search",use_container_width=False):
        if search_term :
            with st.spinper("Searching..."):
                time.sleep(0.5)
                search_books(search_term,search_by)

    if hasattr(st.session_state,'search_results'):
        if st.session_state.search_reasults:
            st.markdown(f"<h3> Found{len(st.session_state.search_reaults)}results:</h1>",unsafe_allow_html=True)

            for i, book in enumerate(st.session_state.search_results):
                st.markdown(f"""
                            <div class ='book-card'>
                            <h3>{book['title']} </h3>
                            <p><strong> Author:<strong> {book['author']}</p>
                            <p><strong> publicaltion year:<strong> {book['publicaltion_year']}</p>
                            <p><strong> Genre:<strong> {book['genre']}</p>
                            <p><span class ='{"read-badge"if book["read_status"]else"unread-badge"}'>{
                                "Read" if book["read_status"] else "Unread"
                            }</span></p>
                            </div>    



""",unsafe_allow_html=True)
        elif search_term:
            st.markdown("<div class ='warning-message'>No books found matching your search.</div>",unsafe_allow_html = True)

elif st.session_state.currend_view =="stats":
    st.markdown("<h2 class ='sub-header'>library statistics</h2>",unsafe_allow_html= True)
    if not st.session_state.library:
        st.markdown("<div class='warning message'> Your library is empty.Add some books to se")
    else:
        stats = get_library_stats()
        col1,col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Books",stats['total_books'])
        with col2: 
            st.metric("Book Read",stats['read_books'])
        with col3:
            st.metric("Percentage Read",f"{stats['percentage_read']:.1f}%")
        create_vislation()

        if stats['authors']:
            st.markdown("<h3>Top Authors </h3>",unsafe_allow_html=True)
            top_authors = dict(list(stats['authors'].items())[:5])
            for author, count in top_authors.items():
                st.markdown(f"**{author}**:{count}book{'s'if count> 1 else ''}")
st.markdown("---")
st.mardown("Copyrigth @ 2025 Prithvi kishan personal library Manager",unsafe_allow_html =True)




    
