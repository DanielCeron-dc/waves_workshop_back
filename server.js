const express = require("express");
const bodyParser = require("body-parser");
const cors = require("cors");
const { exec } = require("child_process");
const path = require("path");

const app = express();
app.use(bodyParser.json());
app.use(cors());

app.post("/run", (req, res) => {
    const { time } = req.body;
    const outputPath = path.join(__dirname, "output.mp4");

    const pythonScriptPath = path.join(__dirname, "workshop1_5.py");
    const command = `python "${pythonScriptPath}" --time ${time} --output "${outputPath}"`;

    exec(command, (error, stdout, stderr) => {
        if (error) {
            return res.status(500).send({ error: stderr });
        }
        res.sendFile(outputPath);
    });
});

const PORT = 5000;
app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});