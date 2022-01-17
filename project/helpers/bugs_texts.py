from project.setup_ import defaults as d


_bug_sessions = [
    # session 0
    {"number": 0, "title": "Welcome", "game_id": d.Admin.id},
    # session 1
    {"number": 1, "title": "Comments/suggestions", "game_id": d.Admin.id},
    # session 2
    {"number": 2, "title": "Bugs-Display", "game_id": d.Admin.id},
    # session 3
    {"number": 3, "title": "Bugs-Crash-the-app", "game_id": d.Admin.id},
    # session 4
    {"number": 4, "title": "Bugs-Unexpected-behavior", "game_id": d.Admin.id},
    # session 5
    {"number": 5, "title": "Bugs-Other", "game_id": d.Admin.id},
]


_bug_texts = [
    # session 0
    {
        "session_number": 0,
        "game_id": d.Admin.id,
        "text": "<p><strong class='ql-size-large'>Welcome to the bug report and comment page!</strong></p><p><br></p><p>This is a place where you can help us out by reporting issues that you find on the site, suggesting ideas ways you think it could be improved or just sending us love letters.</p><p><br></p><p>All comments/suggestions are welcome, and we will read through them all. To limit clutter try to post in the appropriate section by clicking the tab to the left, and before reporting or commenting check to see if someone else has already posted the same thing, but if you have something new to add, don't be shy to make your own note about it.</p><p><br></p><p>Thank you so much for helping us improve Chonicler!!</p>",
    },
    # session 1
    {
        "session_number": 1,
        "game_id": d.Admin.id,
        "text": "<p><strong class='ql-size-large'>Post all of your brilliant suggestions here!</strong></p><p><br></p><p>...or just anything that doesn't fit anywhere else</p>",
    },
    # session 2
    {
        "session_number": 2,
        "game_id": d.Admin.id,
        "text": "<p><strong class='ql-size-large'>Post any bugs relating to how things look here.</strong></p><p><br></p><p>examples of appropriate things would be:</p><ul><li>text and background color clashes that make it hard to read</li><li>something is way bigger or smaller than it should be.</li><li>page element not where it should be</li><li>can't click on something you should be able to click on</li><li>something just looks funky</li></ul><p><br></p><p>When posting here please include whether your browser is running in dark or light mode, and the steps needed to replicate it if applicable.</p>",
    },
    # session 3
    {
        "session_number": 3,
        "game_id": d.Admin.id,
        "text": "<p><span class='ql-size-large'>Post any bugs that crash the application here</span></p><p><br></p><p>if you ever get a server error 500 tell us about it here. Please include steps required to replicate it.</p>",
    },
    # session 4
    {
        "session_number": 4,
        "game_id": d.Admin.id,
        "text": "<p><span class='ql-size-large'>Something not acting like it should? Let us know here.</span></p><p><br></p><p>examples of appropriate things would be:</p><ul><li>link taking you to the wrong location</li><li>able to edit a note that isn't yours</li><li>incorrect image attached to character</li><li>page not found</li></ul><p><br></p><p>as always please try to give us as much information you can about how to reproduce the bug so we can track it down</p>",
    },
    # session 5
    {
        "session_number": 5,
        "game_id": d.Admin.id,
        "text": "<p><span class='ql-size-large'>Your bug/comment/suggestion/love-letter doesn't quite fit anywhere else? Post it here!</span></p><p><br></p><p>expample of appropriate things to post here would be:</p><p><br></p><ul><li>...I have no idea</li></ul>",
    },
]
