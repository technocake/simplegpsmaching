Structure:


fileread.py
-----------

Reads the plt trajectory files in the Data/ folder and generates the matrix.npy numpy array.

makecontactgraph.py
-------------------

Reads matrix.npy and builds a contact graph (as "contactgraph50.3.zip")


Graph structure:

- The nodes in the graph represent people.
- The edges in the graph represent a contact between people (together within 50m for 1 minute).
- Each contact each has additional attributes:
   
    

contactgraph.py
-------------------

Reads the contact graph and peforms analysis



TODO:
- write function to remove graph edges that represent contacts older than two weeks.
