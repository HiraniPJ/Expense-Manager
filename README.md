<h1>Expense Manager</h1>
<h2><b>Overview</b></h2>
<p>Expense Manager is a tool designed to help individuals and families keep track of their monthly expenses efficiently using Google Spreadsheets. This system simplifies financial monitoring and budgeting, offering users an intuitive interface to input, analyze, and visualize their spending habits over time.</p>

<p>The application is available for viewing <a href="https://expense-manage-bc56a7dbb585.herokuapp.com/">Expense Manager</a></p>

<p>The Google sheet for this application is available for use <a href="https://docs.google.com/spreadsheets/d/1zNxBW0gxPYfTkYzdfDj7M-JjDe_q-cyNATAsHJw3WnI/edit#gid=0">Expense-Manager</a></p>


<h2><b>Goals</b></h2>
<p>The primary goal of Expense Manager is to provide a user-friendly platform that makes the task of managing personal finances easy and accessible for everyone, regardless of their technical expertise. The system aims to encourage better financial management and planning.</p>

<h2><b>User Stories</b></h2>
<ul>
<li>As a user, I want to: easily enter my expenses, so I can keep accurate track of my spending without much effort.</li>
<li>As a budget-conscious individual, I want to: visualize my monthly spending patterns, so I can identify areas where I can save money.</li>
<li>As a family, we want to: monitor our collective expenses, to ensure we stay within our budget each month.</li>
</ul>

<h2><b>UX Goals</b></h2>
<ul>
<li>User-Friendly Interface: Easy navigation and minimalistic design.</li>
<li>Quick Data Entry: Streamlined process for entering expenses.</li>
<li>Comprehensive Reporting: Visual charts and categorized expenses.</li>
</ul>

<h2><b>Structure</b></h2>
<ul>
<li>Select Month for input.</li>
<ol>
<li>January</li>
<li>February</li>
<li>March</li>
<li>April</li>
<li>May</li>
<li>June</li>
<li>July</li>
<li>August</li>
<li>September</li>
<li>October</li>
<li>November</li>
<li>December</li>
</ol>
<li>Input the number of the month with validation.</li>
<li>Budget input prompt.</li>
<li>Option to log the expense on the spreadsheet.</li>
<li>List of categories of expenses for selection.</li>
<ol>
<li>Rent</li>
<li>Groceries</li>
<li>Vehicle</li>
<li>Cafe/Restaurant</li>
<li>Online Shopping</li>
<li>Other</li>
</ol>
<li>Category input prompt.</li>
<li>Expenses spend prompt with validation.</li>
<li>Generate expense report prompt with validation.</li>
<li>Visual report of the monthly expense potrayed on a table format.</li>
</ul>

 <h2><b>Scope of Application</b></h2>
 <p>Expense Manager aims to cater to individuals looking for a simple yet effective way to track their personal finances, especially suited for those who prefer using Google Spreadsheets for data management.</p>

<h2><b>Strategy</b></h2>
<h3>Target Audience</h3>
<ul>
<li>Young adults managing their finances for the first time.</li>
<li>Experienced budgeters looking for a straightforward solution.</li>
</ul>
<h3>Key Information Deliverables</h3>
<ul>
<li>Monthly expense summary.</li>
<li>Category-wise spending breakdown.</li>
<li>Budget comparison insights.</li>
</ul>
<h3>Visual Simplicity</h3>
<p>The interface is designed with a focus on clarity and minimalism to prevent user fatigue and enhance readability.</p>

<h2>Aesthetics</h2>
<p>The UI will use a calm color palette to encourage stress-free financial management and incorporate responsive design principles to ensure functionality across devices.</p>

<h2>Wireframes/Flowchart</h2>


<h2><b>Features</b></h2>
<p>Monthly Budget Setting: Set a monthly budget for various categories.</p>
<img src ="Assets/readmeimages/budget.setting.png" alt ="Monthly Budget">
<p>Expense Logging: Log expenses by category for any selected month.</p>
<img src ="Assets/readmeimages/expense.logging.png" alt ="Expense Logging">
<p>Report Generation: Generate and view a monthly expense report.</p>
<img src ="Assets/readmeimages/generate.report.png" alt ="Report Generation">

<h2><b>Technologies</b></h2>
<ul>
<li>Python: Python 3.8 or above.</li>
<li>Google Sheet API: Manage and store data.</li>
<li>gspread: Python API for Google Sheets.</li>
<li>PrettyTable: For displaying data in a tabular format in the console.</li>
<li>Termcolor & Colorama: For colored console output.</li>
<li>Art: For ASCII art representations.</li>
</ul>

<h2><b>Validator Testing</b></h2>
<p>Expense Manager app was tested using Python Linter, and the following are the initial Results of the errors. <p>
<li>21: E302 expected 2 blank lines, found 1</li>
<li>22: E117 over-indented</li>
<li>24: W293 blank line contains whitespace</li>
<li>25: E302 expected 2 blank lines, found 1</li>
<li>28: W291 trailing whitespace</li>
<li>31: W293 blank line contains whitespace</li>
<li>42: W293 blank line contains whitespace</li>
<li>47: E501 line too long (128 > 79 characters)</li>
<li>53: W291 trailing whitespace</li>
<li>55: E211 whitespace before '['</li>
<li>57: W293 blank line contains whitespace</li>
<li>66: W291 trailing whitespace</li>
<li>87: W291 trailing whitespace</li>
<li>93: E501 line too long (84 > 79 characters)</li>
<li>99: E303 too many blank lines (3)</li>
<li>105: W293 blank line contains whitespace</li>
<li>121: E303 too many blank lines (3)</li>
<li>128: W293 blank line contains whitespace</li>
<li>141: W291 trailing whitespace</li>
<li>159: E303 too many blank lines (3)</li>
<li>177: E501 line too long (84 > 79 characters)</li>
<li>181: E305 expected 2 blank lines after class or function definition, found 1</li>
<li>181: E225 missing whitespace around operator</li>

<p>The errors were tthen later fixed and here is the final results of the Testing</p>

<img src="Assets\readmeimages\pythonlinternoerror.JPG" alt = "Test-Results">

<h2>Github Process</h2>

<h3>Fork</h3>
<ol type="1.">
<li>On GitHub.com, navigate to the HiraniPJ/Expense-Manager repository.</li>
<li>In the top-right corner of the page, click Fork.</li>
<li>By default, forks are named the same as their parent repositories. You can change the name of the fork to distinguish it further.</li>
<li>Add a description to your fork to indicate that this is your personal copy or a place where you're planning to propose changes.</li>
<li>Click Create fork.</li>

<h3>Clone</h3>
<ol type="1.">
<li>Above the list of files, click the button that says 'Code'.</li>
<li>Copy the URL for the repository.</li>
<li>Open Terminal. Change the directory to the location where you want the cloned directory.</li>
<li>Type git clone, and then paste the URL you copied earlier.</li>
<li>Press Enter.</li>

<h3>Local Deployment</h3>
<ol type="1.">
<li>Sign up to Gitpod or any other online IDE that suits your development needs.</li>
<li>Download the Gitpod browser extension for easy access.</li>
<li>On GitHub.com, navigate to the HiraniPJ/Expense-Manager repository.</li>
<li>Above the list of files, click the button that says 'Gitpod'.</li>
<li>This will open a new Gitpod workspace with your cloned repository ready to use.</li>

<h2><b>Heroku Deployment</b></h2>


<h1><b>Credits</b></h1>


<h2><b></b></h2>
<h2><b></b></h2>
<h2><b></b></h2>
<h2><b></b></h2>
<h2><b></b></h2>
<h2><b></b></h2>
<h2><b></b></h2>
<li></li>
<li></li>
<p></p>
<p></p>
<p></p>
<p></p>
<p></p>
<p></p>
<p></p>
<p></p>