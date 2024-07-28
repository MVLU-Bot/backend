# import markdown

markdown_values = [
    '''
    MVLU College offers a variety of undergraduate courses, including:

    * **Bachelor of Science in Information Technology (BSc IT)** 
    * **Bachelor of Science in Biotechnology (BSc Biotechnology)**
    * **Bachelor of Arts in Multimedia and Mass Communication (BAMMC)**
    * **Bachelor of Science in Computer Science (BSc CS)**

    These courses provide students with a strong foundation in their chosen field and prepare them for successful careers in various industries.
    ''',
    '''
    Our college library is a haven for knowledge seekers, offering a tranquil and conducive environment for students to immerse themselves in their academic pursuits. It boasts an extensive collection of books, reference materials, and digital resources that cater to the needs of various courses and disciplines.  
    
    ![Photo of Library](https://res.cloudinary.com/dglnosi2i/image/upload/f_auto,q_auto/v1/mvlubot/Library)
    ''',
]

message_cache = {
    "/version": "0.0.1",
    "hi": "Hi! 👋 \n\nI'm here to help you with any questions you may have about MVLU College.  What can I help you with today? \n",
    "hello": "Hello! 👋  How can I help you today? 😊 \n",
    "What are the courses offered by the college?": markdown_values[0],
    "Tell me something about the college Library?": markdown_values[1],

}

# print(markdown.markdown(markdown_values[0]))