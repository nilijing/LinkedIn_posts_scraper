# LinkedIn_posts_scraper


The main function of the project is to fetch posts published by companies or users on LinkedIn and then save content that we need into mysql database.
The info we wanna reorganize includes description of the posts, hashtags, published time, scraped time, and related links both attached with image or the content.

<br>
Hence, I picked Google as a template to analysis its posts published on their LinkedIn: https://www.linkedin.com/company/google/posts/?feedView=all

Take one post analysis as an example:

<img src="https://raw.githubusercontent.com/nilijing/LinkedIn_posts_scraper/main/image/Screen%20Shot%202021-03-05%20at%202.39.56%20PM.png" width="500" />
Lastly，use sqlalchemy to connect with mysql to save the search results as below.
<img src="https://raw.githubusercontent.com/nilijing/LinkedIn_posts_scraper/main/image/Screen%20Shot%202021-03-05%20at%2010.45.57%20PM.png" width="800" />

<br>
In addition,I want to introduce you all a useful post inspector tool: https://www.linkedin.com/post-inspector/. It retrive articles posted on LinkedIn by theirs urls. The result not only provide general info like post published time but also include the writer.
