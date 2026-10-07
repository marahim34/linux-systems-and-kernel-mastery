4. Allocate your object...
5. ...and link it in with list_add_tail (or list_add for the front).
6. list_for_each_entry iterates, giving you each CONTAINING object directly (it uses container_of internally). No casts,
no node objects.