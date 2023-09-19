from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def hello_world():
    return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
<script
  src="https://code.jquery.com/jquery-3.7.1.min.js"
  integrity="sha256-/JqT3SQfawRcv/BIHPThkBvs0OEvtFFmqPF/lYI/Cxo="
  crossorigin="anonymous"></script>
    <title>Title</title>
</head>
<body>
<form id="form_id" action="javascript:post_query()">
    <label>화씨는</label>
    <input type="text" name="temp_f">
    <button type="submit">변환하기</button>
</form>
<div id="results" style="width:50px; height:30px; background-color:#f5d682"></div>
<script>
function post_query() {
    $.ajax({
        type: "GET",
        url: "http://113.198.38.235:5000/f2c",
        data: $("#form_id").serialize(),
        success: update_result,
        dataType: "html"
    });
    }
    function update_result(data) {
        $("#results").html(data);
}
</script>
</body>
</html>"""

@app.route("/f2c")
def f2c():
    temp_f = int(request.args.get("temp_f"))
    return f"{(temp_f - 32) * 5 / 9:.2f}℃"


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")