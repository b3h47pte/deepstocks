const {app, BrowserWindow, Menu} = require('electron');
const {exec} = require('child_process');
const program = require('commander');

program
    .option('--db <database>');

program.parse(process.argv);

let win;

function start() {
    // Start API server python backened.
    exec('apiServer.py --db ' + program.db, (err, stdout, stderr) => {
        console.log(err);
        console.log(stdout);
        console.log(stderr);
    });

    win = new BrowserWindow({
        width: 1280,
        height: 720,
        webPreferences: {
            nodeIntegration: true
        }
    });

    win.setMenu(null);
    win.setMenuBarVisibility(false);
    win.loadFile('index.html');
    win.webContents.toggleDevTools();
}

app.on('ready', start);
app.on('window-all-closed', () => {
    app.quit();
});

