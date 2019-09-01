Alchemical Finances - Manual Personal Finances
Alpha Version 1.7 - 20190901
Beaker Labs llc. [Comming? Different Name?]

------------------------------------------------------------------
Description / Purpose of the Project:
------------------------------------------------------------------
--- The project is designed to replace the use of Microsoft Excel for the purposes of tracking a users Personal Finances 
without the need to move to a program like Mint.com / Quicken / Personal Capital ect. This provides a few benefits such as:
--- -- [A] No 2nd/3rd party Data Mining of user information
--- -- [B] All Data is currently stored on the Users Computer only 
--- -- [C] No Automatically filled ledgers
--- -- [D] Ability to attached Invoices/Receipts to all transactions. 
--- -- [#] Future features are planned [See Bottom for mini pipeline]
--- The program is built on the concept that people understand their finances better when they interact with them rather than watch them.
Having the user manually input transactions helps them pay attention to their exspenses and helps them feel in control. The future addition of
graphs/generated budgets will reinforce this. [Generated budgets will be built from past input data by user selected Categories. Then allow the user to build the following months budget]

------------------------------------------------------------------
Request to Testers
------------------------------------------------------------------
--- Please break my program! Find where my coding needs some work and could benefit from some additional attention. Some things to consider
---  -- - Test User Inputs, Creating New Accounts, Posting/Selecting/Updating/Deleting Transactions, account details ect. Basically everything at this point.
--- Critique the design and concept. At heart the project is meant for me to replace excel but I would like to share to those interested.

------------------------------------------------------------------
Pre-Requisites:
------------------------------------------------------------------
--- Current Design should not require the installation of any additional software. The .exe file should take work independandtly 
--- PyQt5 5.11.2 and Python 3.7 used to code the program

------------------------------------------------------------------
Installation 
------------------------------------------------------------------
Python
--- 1 -- Download all files in the repository. 
--- 2 -- Load the program from the Executable.pyw file.

Executable
[Not Found on Github.]
[https://www.dropbox.com/sh/6hauvozh5ybaoad/AADGMWIEWYdYI-hOdPKZ3DCFa?dl=0]
--- 1 -- Download the entire "Alchemical Finance" directory from Dropbox
--- 2 -- Within the "Alchemical Finance" directory is Alchemical Finances.exe
---   -- - The .exe file was made using pyinstaller
         pyinstaller --onedir --windowed Executable.pyw --name="Alchemical Finances" --icon=AFLogo.ico
***Warning*** --- I find that AntiVirus likes to quarrintine the application. Currently unsure how to work around that. 
--- 3 -- I recommend creating a shortcut and putting that where you find most accessable.
--- 3 -- Data/Receipt directories will be found within the "Alchemical Finances" Directory
--- 4 -- Application should be good to go.
      --  - When creating a new user there may be a delay between the Welcome Message and the MainWindow loading. This is the program generating the user.

------------------------------------------------------------------
Create New User
------------------------------------------------------------------
--- 1 -- Click New Profile
--- 2 -- User Profile is not case sensitive. Everything will be made lowercase.
--- 3 -- Password must be more than 6 characters long and must be alphanumeric. 
---   -- -- Unallowed symbols: ["~", "!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "=", ":",
                     		"+", "<", "?", ";", "'", "[", "]", "{", "}", '"', "-", ".", ","]
--- 4 -- Submit new profile
--- 5 -- Cancel out of the new profile screen
--- 6 -- Login
  
------------------------------------------------------------------
User Manual
------------------------------------------------------------------
--- The file USER_MANUAL.pdf can be found in the same directory as this README.txt.
--- The User Manual will include images and full instructions/conceptual comments about the program.  
--- The User Manual will be accessable from within the program as well. 
   
------------------------------------------------------------------
Data Storage
------------------------------------------------------------------
--- All User information will be stored locally on the system in the directory the program was installed on. All files will be created within the "dist/Executable" directory
--- if you move the program be sure to move the data and receipt files as well or the program will create new ones.
--- User data is stored in the data directory
--- Receipts are stored in the Receipts directory by profile name then account ledger

  
------------------------------------------------------------------
Pipeline Production - Overview room to expand/Change
------------------------------------------------------------------	 
--- 1  -- Equity and Retirement Ledger [COMPLETED]
--- 2  -- Summary Tab [COMPLETED]
---    -- Archive Tab [COMPLETED]
---    -- About Tab [COMPLETED]
---    -- User Manual [COMPLETED]

~~ Anticipating to pivot to a Django Project to mirror/compliment this project. Also helps to avoid burn out.
~~ This is a passion project and it will grow. I also want to share via a blog some additional insight/thoughts

--- 3  -- Saving databases - Program Creates a temp file, then saves over the primary .db File
--- 4  -- Generating Printable Reports
--- 5  -- CSV exporting
--- 6  -- User Data Back-up
--- 7  -- Ledger to track Large Exspense Purchases
--- 8  -- Ledger to track Long Term Projects
--- 9  -- Work on Ui to adjust to user display. [Completed?]
--- 10  -- Rebrand website to destribute program
       -- -- Purchase Commercial Version of PyQt5
       -- -- Find Initial Beta Testers
       -- -- Will make Visual instructions
	   -- -- Include Blog
	   -- -- Comparison to Mint.com and Personal Capital (Maybe Quicken)
--- 11 -- Graphs for budgeting and Net Worth Tracking 
--- 12 -- Expand Receipt Display to have a few more features
--- 13 -- Encryption
--- 14 -- User E-mail Address to reset lost passwords
--- 15 -- Explore taking the program to server/cloud storage
--- 16 -- Explore E-mail notifications
       -- -- User Set reminders
	   -- -- Bills Due? Maintence Due? ect?
--- 17 -- Explore Andriod app

-- Maybe -- Webscrapping some Equity Data -- Unsure at this time if i will dive into webscrapping
-- Maybe -- Ledger to track subscriptions
