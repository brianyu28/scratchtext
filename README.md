<img src="static/title.png" alt="ScratchText" width="600">

A text-based interface for Scratch programming

## About

This is a work in progress for HGSE's T217 Spring 2020.

## First Program

1. Visit http://scratchtext.brianyu.me/
2. Drag the `when_flag_clicked()` block from the **Events** section of the sidebar into the code editor. Your program should now look like:

```
when_flag_clicked() {

}
```

3. Drag the `move(10)` block from the **Motion** section of the sidebar into the code editor. Your program should now look like:

```
when_flag_clicked() {
    move(10)

}
```

4. Drag the `think("Hmm....")` block from the **Looks** section of the sidebar into the code editor. Your program should now look like:

```
when_flag_clicked() {
    move(10)
    think("Hmm...")

}
```

5. Replace the `"Hmm..."` text in the code editor with something other text (e.g. `"Hello!"`). Your program should now look like:

```
when_flag_clicked() {
    move(10)
    think("Hello!")

}
```

6. Click "Download Program" to download a file (called `project.sb3`) to your computer.
7. Visit http://scratch.mit.edu/create to visit Scratch's user interface.
8. From the **File** menu, choose **Load from your computer** and pick your `project.sb3` file. When you're asking to "Replace contents of the current project?", choose **OK**.
9. You should now see your Scratch program loaded as blocks. Click the green flag to run the program, and your sprite should move and think `"Hello!"` (or whatever text you chose).
