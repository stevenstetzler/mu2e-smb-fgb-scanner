
import java.io.*;
import java.nio.file.*;
import static java.nio.file.StandardWatchEventKinds.*;
import java.nio.file.WatchEvent.Kind;
import java.util.logging.Level;
import java.util.logging.Logger;

/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

/**
 *
 * @author Steven
 */
public class FileListener implements Runnable {
    Path listenPath;
    ScannerUI instance;
    boolean bRun = true;
    
    public FileListener(String s, ScannerUI ui) {
        listenPath = Paths.get(s);
        instance = ui;
    }
    
    @Override
    public void run() {
        WatchService watcher = null;
        try {
            watcher = FileSystems.getDefault().newWatchService();
        } catch (IOException ex) {
            Logger.getLogger(FileListener.class.getName()).log(Level.SEVERE, null, ex);
        }
        Path dir = listenPath;
        try {
            WatchKey key = dir.register(watcher,
                                   ENTRY_CREATE);
        } catch (IOException x) {
            System.err.println(x);
        }

        while (true) {

            // wait for key to be signaled
            WatchKey key;
            try {
                key = watcher.take();
            } catch (InterruptedException x) {
                return;
            }

            for (WatchEvent<?> event: key.pollEvents()) {
                WatchEvent.Kind<?> kind = event.kind();

                // This key is registered only
                // for ENTRY_CREATE events,
                // but an OVERFLOW event can
                // occur regardless if events
                // are lost or discarded.
                if (kind == OVERFLOW) {
                    continue;
                }

                // The filename is the
                // context of the event.
                WatchEvent<Path> ev = (WatchEvent<Path>)event;
                Path filename = ev.context();

                // Verify that the new
                //  file is a text file.
                try {
                    // Resolve the filename against the directory.
                    // If the filename is "test" and the directory is "foo",
                    // the resolved name is "test/foo".
                    Path child = dir.resolve(filename);
                    try {
                        if (!Files.probeContentType(child).contains("image")) {
                            System.err.format("New file '%s'" +
                                " is not an image file.%n", filename);
                            continue;
                        }
                        try {
                            Thread.sleep(3000);
                        } catch (InterruptedException ex) {
                            Logger.getLogger(FileListener.class.getName()).log(Level.SEVERE, null, ex);
                        }
                        instance.directoryChangeAction(filename.toString());
                        instance.test(new File(filename.toString()));
                    } catch (NullPointerException e) {
                        continue;
                    }
                } catch (IOException x) {
                    System.err.println(x);
                    continue;
                }

                // Email the file to the
                //  specified email alias.
                System.out.format("Processing image %s%n", filename);
                //instance.directoryChangeAction(filename.toString());

            }

            // Reset the key -- this step is critical if you want to
            // receive further watch events.  If the key is no longer valid,
            // the directory is inaccessible so exit the loop.
            boolean valid = key.reset();
            if (!valid) {
                break;
            }
        }
    }  
}
