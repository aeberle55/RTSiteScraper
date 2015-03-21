# RTSiteScraper

This set of scripts is designed to find and view connections on the Roosterteeth site. It was written for fun, so feel free to fork it and play arround. I make absolutly no guarnetees about the quality of the code. But you probably want to read the comments. They tend to be pretty descriptive. Below is a list of scripts and how to use them.

## scrapeUsers.py

Takes one or more users as seeds, gathers their user data, and repeats the process on their friends if the friends have at least a certain number of friends. The resulting list of users and information is pickled and stored along with a log file. Note that this is a very long process. Let it run overnight, at least. It also cannot be interrupted.

'PKL_FILE' is the location the pickle file containing users will be stored.

'LOG_FILE' is the location the text log file is stored.

'queue' is the queue of usernames waiting to be processed. Enter seeds here.

'THRESHOLD' is the minimum number of friends needed to qualify to be added to the list.

'MAX_PROCESS' is the maximum number of users the program will process. Use if the process may take too long at the current threshold.

## usr.py

This contains the 'user' class used to store user info. Just a bunch of accessor methods, really.

## cAndC.py

Used to get a list of Cast and Crew from an external website. Had to use roosterpedia because the Cast and Crew page on RT is incomplete.

## buildNetworkGraph.py

The meat of the processing. Creates a visual representation the users and their friendship connections. Building a good network graph requires a lot of tweaking of variables, so work at it.

'NODE_SIZE' controls what determines the size of the nodes on the graph. It takes a string. Options are 'friends', 'date', 'karma', and 'none'. The more friends or karma, or the earlier the sign up date, the bigger the nodes for the respective options.

'FILTER_BY' controls what users are included in the graph. Takes a string argument of 'friends', 'date', 'karma', or 'none'. With none, no normal users can be added. The others have their own filtering variables.

'MAX_YEAR' and 'MIN_YEAR' are part of the 'date' filter. They are the two digit year of sign up. Users must have signed up between the years (inclusive) to be in the graph.

'MIN_FRIENDS' and 'MAX_FRIENDS' are part of the 'friends' filter. Same deal as above, except 'MAX_FRIENDS' can take an argument of 'None' to have no maximum.

'MIN_KARMA' and 'MAX_KARMA' It's late. You get the idea.

'FONT_SIZE' is an integer specifying the font size of the usernames.

'K_VAL' is a constant used by the position algorithm, and may be 'None' or a double in the range of (0,1). A higher number has it try to push the nodes further appart. Leave as 'None' to have it computed automatically.

'NUM_ITERATIONS' is the number of iterations of the position algorithm. A higher number takes longer to compute and may not be better, but often is.

'PKL_FILE' is the location of the file of users.

'CC_LIST' is the location of the file containing a list of Cast and Crew. If the file doesn't exist, it will be populated and generated at this location.

'IMG_FILE' is the location the image of the graph will be stored.

'HIST_FILE' is the location the optional degree histogram will be stored.

'FIG_SIZE' is the size of one side of the graph in hundreds of pixels. The bigger, the longer the position algorithm takes. I've also found around a 22,000 x 22,000 image is the max a computer can handle. If you see a segfault, make this smaller.

'INCLUDE_CC' Determines how the Cast and Crew are treated. 0 excludes them, 1 treats them like a normal user, and 2 allows them to bypass filters.

'GET_HIST' causes a degree histogram to be generated if true.

'LOG_LOG' causes the histogram to use a Log-Log plot.

## Colors and Weights

Nodes and edges are colored. Edges also have different thicknesses. The explanations are below.

'Node Colors:'
Red     -       Cast and Crew

Blue    -       Male

Pink    -       Female

Grey    -       Gender not Available

'Edge Colors'

Red     -       Friendship between two Cast and Crew

Blue    -       Friendship between two Males

Pink    -       Friendship between two Females

Grey    -       Friendship between two users of unspecified gender

Purple  -       Friendship between user and staff

Green   -       Friendship between users of different genders

'Edge Weights'

Heavy   -       Friendship between two staff

Medium  -       Friendship between staff and user

Light   -       Friendship between two users
