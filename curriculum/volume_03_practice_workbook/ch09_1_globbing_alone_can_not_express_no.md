1. Globbing alone can not express 'NOT these characters' across a whole name, so we pipe the listing to grep. Inside
the bracket the leading ^ means NEGATE, so this finds any name containing a character outside the allowed set:
spaces, quotes, and other troublemakers.

3.6 No digit in 2nd and 4th position
List names where characters two and four are not digits.





ls ?[^0-9]?[^0-9]*