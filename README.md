Installation
============

```
pip install -r requirements.txt
```


Structure
=========


fileread.py
-----------

Reads the plt trajectory files in the Data/ folder and generates the matrix.npy numpy array.

makecontactgraph.py
-------------------

Reads matrix.npy and builds a contact graph (as "contactgraph50.3.zip")


Graph structure:

- The nodes in the graph represent people.
- The edges in the graph represent a contact between people (at least one contact within 50m for 1 minute).
- Each contact edge each has the list of contacts as an additional attribute. This list stores details of each contact. Specifically, it stores:
  - Start and endposition of contact (lat/lon).
  - Start and endtime of contact 
  - Minimal/Maximum/Average distance of contact
  - Movement type for both people (e.g. metro, walking, ...)
    

contactgraph.py
-------------------

Reads the contact graph and peforms analysis



TODO
====
- write function to remove graph edges that represent contacts older than two weeks.
