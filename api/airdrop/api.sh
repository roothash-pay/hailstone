curl --location --request POST 'http://127.0.0.1:8000/api/get_points_by_address' --header 'Content-Type: application/json' --data-raw '{"address": "0xe3b4ECd2EC88026F84cF17fef8bABfD9184C94F0" }'


curl --location --request POST 'http://127.0.0.1:8000/api/get_points_record_by_address' --header 'Content-Type: application/json' --data-raw '{"address": "0xe3b4ECd2EC88026F84cF17fef8bABfD9184C94F0" }'