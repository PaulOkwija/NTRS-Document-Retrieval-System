# NASA_SPACE_APPS_CHALLENGE
 This is the implementation of the document retrieval system for the NASA Technical Reports Server (NTRS) for the 2022 NASA Space Apps challenge
Corpus

Given the large number of documents in the NTRS, we use the NASA NTRS OpenAPI to automatically download legacy documents instead of manually navigating the database. This saves time and is more efficient.

We download documents belonging to 3 randomly chosen broad topics. For each broad subject category, we randomly select 2 specific subject categories. We follow the existing NASA STI Scope and Subject Category Guide when selecting these categories.

For each document in the corpus, the corresponding metadata such as document id, title, and abstract are saved in JSON files.

Assigning keywords to documents

Since each document in the NTRS has a subject category assigned to it, we obtain the corresponding keywords for that subject category. For each document in a given category, we assign the relevant keywords by finding the similarity between the document and all the keywords in that category. The keywords are then added to the corresponding JSON files.

Web application

We then developed a web-based application integrated with Natural language processing algorithms that can retrieve documents from the National Technical Report Server based on a query. The application has two features: the filter feature and the search feature.

The filter feature allows the user to filter the documents based on the subject categories. The search feature allows a user to input a query into a search bar and tap the search button to retrieve documents based on that query.

The titles, abstracts or summaries, keywords, and text analytics of the retrieved documents are then displayed on the web application interface.



Back-End

The back-end consists of three systems: the retrieval system, the text summarization system, and the text analytics system. These systems utilize natural language processing techniques to perform their respective tasks.

For the filter feature, the retrieval system returns all documents belonging to the selected subject category. For the search feature, the retrieval system compares the query with all the documents in the corpus by calculating a similarity score between the query vector and the corpus vector.

The text summarization system extracts the abstract for the returned documents. If the document does not have an abstract, the system generates an abstract for the document.

The text analytics system analyzes the contents of the whole document and retrieves relevant keywords, topics, and other related analytic information. 

Front-End

The web application, with which users interface, was created using stream-lit to provide a user-friendly way of utilizing our solution. The image below shows the appearance of the interface before a query is made.



After a query is made the results are displayed on the web interface as shown in the image below.



Our solution improves the accessibility and discoverability of legacy documents by providing relevant information such as keywords, subject topics, abstracts, and summaries that guide researchers to find the desired information.

Future Work 

We intend to include a feature that translates the document summaries into African languages so as to encourage more Africans into space research. We shall also extract images from these documents to generate a simple animation returned besides the abstract/summary to give researchers more insights into the documents.
