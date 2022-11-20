
# GenApi

REST API for the *Artifindr* project's face generation.

## HTTP request endpoints

For new* images use:
>GET genapi/

For images with determined seeds (e.g., for corrupted/missing data replacement) use:
>GET genapi/:seed

Please note that this API is stateless, meaning all data sent back is dynamically generated and **is not stored** in any way.

*- *seeds are by convention a hundred integers long, so while possible, repeated results are highly unlikely*

