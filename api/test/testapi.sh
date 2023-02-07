(echo -n '{"image": "'; base64 $1; echo '"}') | curl -H "Content-Type: application/json" -d @- http://127.0.0.1:5000/predict
echo