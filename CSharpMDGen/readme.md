*Sample CSharp MDGen Code*

```csharp
// create our MDFile object
MDFile file = MDGen.Create();

// create sections
var intro = MDGen.CreateSection("Introduction", "This is the introduction section.", "Arial");
var gettingStarted = MDGen.CreateSection("Getting Started", "This is the getting started section.", "Arial");
var advanced = MDGen.CreateSection("Advanced Topics", "This is the advanced topics section.", "Arial");
var tableSection = MDGen.CreateSection("Table", "", "Arial");
var coloredUL = MDGen.CreateSection("Colored Unordered List", "This section contains a colored unordered list.", "Arial");

// create a code block
string code = "Console.WriteLine(\"Hello World!\");";
var codeBlock = MDGen.CreateCodeBlock(code, "csharp", "Hello World Example:");

// add padding to the code block to make it easier to read
MDGen.AddCodeBlockPadding(codeBlock, false, 1);

// add the code block to the intro section
MDGen.AddCodeBlock(intro, codeBlock);

// create an unordered list
string[] items = ["Item 1", "Item 2", "Item 3"];
var ul = MDGen.CreateUL(items, "Unordered List:", headingSize: 3);

// create an ordered list
string[] items2 = ["Item 1", "Item 2", "Item 3"];
var ol = MDGen.CreateOL(items2, "Ordered List:");

// add our ordered list to the advanced section


MDGen.AddListElement(gettingStarted, ul, ordered: false);
MDGen.AddListElement(advanced, ol, ordered: true);

// create a table
string[] headers = ["Left", "Center", "Right"];
int[] alignment = [0, 1, 2];
string[,] rows = {
    { "Column 1 Row 1", "Column 2 Row 1", "Column 3 Row 1" },
    { "Column 1 Row 2", "Column 2 Row 2", "Column 3 Row 2" },
    { "Column 1 Row 3", "Column 2 Row 3", "Column 3 Row 3" }
};
Table table = MDGen.CreateTable(headers, alignment, rows);

// add a table 
MDGen.AddTable(tableSection, table);

// add a colored unordered list
UL redUL = MDGen.CreateUL(["Item 1", "Item 2", "Item 3"], "Colored Unordered List:", "Red");
MDGen.AddListElement(coloredUL, redUL, ordered: false, smallTab: true);

// add padding to the end of each section to make it easier to read
MDGen.AddSectionPadding(intro, false, 1);
MDGen.AddSectionPadding(intro, true, 2);
MDGen.AddSectionPadding(gettingStarted, true, 2);
MDGen.AddSectionPadding(advanced, true, 2);

// add sections to file
MDGen.AddSection(file, intro);
MDGen.AddSection(file, gettingStarted);
MDGen.AddSection(file, advanced);
MDGen.AddSection(file, tableSection);
MDGen.AddSection(file, coloredUL);

// write our MDFile object to an MD file
var res = MDGen.WriteToFile(file);

// indicate if the creation was successful
Console.WriteLine(res ? "File created successfully" : "File creation failed");
```
