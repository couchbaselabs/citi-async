BaseRepo.py just holds an interface.
Config.py just creates a class to hold the couchbase settings

Conn.py is where the bulk of the code is.
It uses the acouchbase package. It does not call asycio directly.
