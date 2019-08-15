"use strict";

const {app, BrowserWindow, Menu} = require('electron');

let win;

function start() {
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
