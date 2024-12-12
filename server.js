const express = require("express");
const bodyParser = require("body-parser");
const cors = require("cors");
const { exec } = require("child_process");
const path = require("path");

const app = express();
app.use(bodyParser.json());
app.use(cors());

// Endpoint para el primer script
app.post("/run", (req, res) => {
    const { time } = req.body;
    console.log(req.body);
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

// Endpoint para el segundo script
app.post("/vibration", (req, res) => {
    const { frecuency } = req.body;
    if (!frecuency) {
        return res.status(400).send({ error: "La frecuencia es requerida" });
    }

    const outputPath = path.join(__dirname, "vibration_output.mp4");
    const pythonScriptPath = path.join(__dirname, "workshop1_6.py");

    const command = `python "${pythonScriptPath}" --frecuencia ${frecuency} --output "${outputPath}"`;

    exec(command, (error, stdout, stderr) => {
        if (error) {
            return res.status(500).send({ error: stderr });
        }
        res.sendFile(outputPath);
    });
});

// Endpoint para el tercer script (onda acústica)
app.post("/wave", (req, res) => {
    const { time_wave, range_x } = req.body;

    if (!time_wave || !range_x) {
        return res.status(400).send({ error: "Se requieren los parámetros tiempo y rango_x" });
    }

    const outputPath = path.join(__dirname, "wave_output.mp4");
    const pythonScriptPath = path.join(__dirname, "workshop2_1.py");

    const command = `python "${pythonScriptPath}" --tiempo ${time_wave} --rango_x ${range_x} --output "${outputPath}"`;

    exec(command, (error, stdout, stderr) => {
        if (error) {
            return res.status(500).send({ error: stderr });
        }
        res.sendFile(outputPath);
    });
});

// Nuevo endpoint para el efecto Doppler
app.post("/doppler", (req, res) => {
    const outputPath = path.join(__dirname, "doppler_simulation.mp4");
    const pythonScriptPath = path.join(__dirname, "workshop2_7.py");

    const command = `python "${pythonScriptPath}"`;

    exec(command, (error, stdout, stderr) => {
        if (error) {
            console.error(stderr);
            return res.status(500).send({ error: stderr });
        }
        console.log(stdout);
        res.sendFile(outputPath);
    });
});

const PORT = 5000;
app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
