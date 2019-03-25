const express = require('express')
const app = express()

app.get('/', (req, res) => {
    const { spawn } = require('child_process')
    const faceRecognition = spawn('python3', ['./image_face_detection.py', '--image', 'test_image.jpeg', '--repo', 'images'])
    let data1 = []
    faceRecognition.stdout.on('data', function (data) {
        console.log(data.toString())
        data1.push(data.toString())
    })

    faceRecognition.on('exit', exitCode => {
        console.log(exitCode)
        res.write(data1.toString())
        res.end('end')
    })
})

app.listen(4000, () => console.log("Running on port 4000"))