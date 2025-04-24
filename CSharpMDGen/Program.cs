using System.Text;

namespace CSharpMDGen
{
    public class Program
    {
        public static void Main()
        {
            #region Demo
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
            #endregion
        }
    }
    #region MDGen Functions
    public class MDGen
    {
        // create an MDFile object
        public static MDFile Create(string fn = "file", string title = "My MD File", string font = "Arial")
        {
            // check if the file name is valid
            if (!IsFileNameValid(fn))
            {
                Console.WriteLine("Invalid file name");
                return null!;
            }

            // create an instance of the MDFile object
            MDFile file = new()
            {
                FileName = $"{fn}.md",
                Title = $"# {title}",
                DefaultFont = font
            };

            // return our MDFile object
            return file;
        }

        // create an unordered list object
        public static UL CreateUL(string[] items, string title = null!, string color = "Nothing!", string font = "Aria", int headingSize = 5, bool boldTitle = false)
        {
            // write the user specified information to an instance of the UL object
            UL ul = new()
            {
                Items = items,
                Title = title,
                Color = color,
                Font = font,
                HeadingSize = headingSize,
                BoldTitle = boldTitle
            };
            // return our new UL object
            return ul;
        }

        // create an ordered list object
        public static OL CreateOL(string[] items, string title = null!, string color = "Nothing!", string font = "Arial")
        {
            // write the user specified information to an instance of the UL object
            OL ol = new()
            {
                Items = items,
                Title = title,
                Color = color,
                Font = font
            };
            // return our new UL object
            return ol;
        }

        // create a code block object
        public static CodeBlock CreateCodeBlock(string code, string lang = null!, string title = null!, string color = "Black", string font = "Arial")
        {
            // write the user specified information to an instance of the Code Block object
            CodeBlock cb = new()
            {
                Code = code,
                Lang = lang,
                Title = title,
                Color = color,
                Font = font,
                Finalized = false
            };
            // return our new UL object
            return cb;
        }

        // create a section object
        public static Section CreateSection(string title, string content, string font = null!, string color = "Black")
        {
            // create an instance of the Section object with the info passed into the function
            Section section = new()
            {
                Title = $"### {title}",
                Color = color,
                Font = font,
                Content = content,
                Finalized = false
            };
            // return our Section object
            return section;
        }

        // add a section to our md file after we have created it
        public static bool AddSection(MDFile file, Section section)
        {
            try
            {
                // check if the section exists if it does add to it, else create it
                if (file.Sections != null)
                {
                    file.Sections!.Add(section);
                    // set the section to finalized so it cannot be changed
                    section.Finalized = true;
                }
                else
                {
                    file.Sections = [section];
                    // set the section to finalized so it cannot be changed
                    section.Finalized = true;
                }
            }
            catch
            {
                // if there is an error adding the section to the file, print an error message
                Console.WriteLine("Error adding section to file");

                // return false to indicate the section was not added
                return false;
            }
            // return true to indicate the section was added
            return true;
        }

        // add an unordered list to a section
        public static bool AddUL(Section section, UL ul, bool smallTab = true, bool mdSafe = false)
        {
            // define tab sizes (4 spaces and 2 spaces)
            const String TAB = "    ";
            const String SMALL_TAB = "  ";
            string tab = smallTab ? SMALL_TAB : TAB;

            // if the section is not finalized, add the unordered list to it
            if (section.Finalized == false)
            {
                try
                {
                    if (!string.IsNullOrEmpty(ul.Title))
                    {
                        string tagOpen = ul.BoldTitle ? "<b>" : "";
                        string tagClose = ul.BoldTitle ? "</b>" : "";
                        section.Content += $"\n<h{ul.HeadingSize}>{tagOpen}{ul.Title}{tagClose}</h{ul.HeadingSize}>\n\n";
                    }

                    // add the items in the unordered list to the section with the selected tab size
                    StringBuilder sb = new();
                    foreach (var item in ul.Items)
                    {
                        string style = BuildStyle(ul.Font, ul.Color);
                        if (!mdSafe)
                        {
                            if (style != "")
                                sb.AppendLine($"{tab}- {style}{item}</span>");
                            else
                                sb.AppendLine($"{tab}- {item}");
                        }
                        else
                        {
                            sb.AppendLine($"{tab}- {item}");
                        }
                    }
                    section.Content += sb.ToString();
                }
                catch
                {
                    // if there is an error adding the unordered list to the section, print an error message
                    Console.WriteLine("Error adding unordered list to file");
                    return false;
                }
                return true;
            }
            else
            {
                // if the section is finalized, print an error message
                Console.WriteLine("Section has already been finalized 217");
                return false;
            }
        }

        private static string BuildStyle(string font, string color)
        {
            if (color == "Nothing!" && font == "Arial") return "";

            string style = "";
            if (font != "Arial") style += $"font-family:{font};";
            if (color != "Nothing!") style += $"color:{color};";
            return $"<span style=\"{style}\">";
        }

        public static bool AddListElement(Section section, IListElement list, bool ordered, bool smallTab = true, bool mdSafe = false)
        {
            const string TAB = "    ";
            const string SMALL_TAB = "  ";
            string tab = smallTab ? SMALL_TAB : TAB;

            if (section.Finalized)
            {
                Console.WriteLine("Section has already been finalized");
                return false;
            }

            try
            {
                // Add the list's title as a heading if it exists
                if (!string.IsNullOrEmpty(list.Title))
                {
                    string tagOpen = list.BoldTitle ? "<b>" : "";
                    string tagClose = list.BoldTitle ? "</b>" : "";
                    section.Content += $"\n<h{list.HeadingSize}>{tagOpen}{list.Title}{tagClose}</h{list.HeadingSize}>\n\n";
                }

                // Add the list items
                StringBuilder sb = new();
                int index = 1;
                foreach (var item in list.Items)
                {
                    string style = BuildStyle(list.Font ?? "Arial", list.Color ?? "Nothing!");
                    string prefix = ordered ? $"{index}." : "-";
                    index++;

                    string line;
                    if (!mdSafe && !string.IsNullOrEmpty(style))
                        line = $"{tab}{prefix} {style}{item}</span>";
                    else
                        line = $"{tab}{prefix} {item}";

                    sb.AppendLine(line);
                }

                section.Content += sb.ToString();
                return true;
            }
            catch
            {
                Console.WriteLine("Error adding list element to section");
                return false;
            }
        }

        // add padding to the section to make it easier to read
        public static bool AddSectionPadding(Section section, bool trailing, int padding = 1)
        {
            // if the section is not finalized, add padding to it
            if (section.Finalized == false)
            {
                try
                {
                    // add the padding to the section
                    for (int i = 0; i < padding; i++)
                    {
                        // if the padding is trailing, add it to the end of the section
                        if (trailing)
                            section.Content += "\n";
                        // if the padding is not trailing, add it to the beginning of the section
                        else
                            section.Content = "\n" + section.Content;
                    }
                }
                catch
                {
                    // if there is an error adding the padding to the section, print an error message
                    Console.WriteLine("Error adding padding to section");
                    return false;
                }
                return true;
            }
            else
            {
                // if the section is finalized, print an error message
                Console.WriteLine("Section has already been finalized 296");
                return false;
            }
        }

        // add a code block to a section
        public static bool AddCodeBlock(Section section, CodeBlock codeBlock)
        {
            if (section.Finalized == false)
            {
                try
                {
                    StringBuilder sb = new(section.Content);

                    if (!string.IsNullOrWhiteSpace(codeBlock.Title)) {
                        for (int i = 0; i < codeBlock.Padding; i++)
                            sb.AppendLine("");
                        sb.AppendLine($"\n***{codeBlock.Title}***");
                    }

                    if (!string.IsNullOrWhiteSpace(codeBlock.Lang))
                        sb.AppendLine($"```{codeBlock.Lang}");
                    else
                        sb.AppendLine("```");

                    sb.AppendLine(codeBlock.Code.Trim());
                    sb.AppendLine("```");

                    for (int i = 0; i < codeBlock.Trailing; i++)
                        sb.AppendLine("");

                    section.Content = sb.ToString();
                    codeBlock.Finalized = true;
                    return true;
                }
                catch
                {
                    Console.WriteLine("Error adding code block to section");
                    return false;
                }
            }
            else
            {
                Console.WriteLine("Section has already been finalized 333");
                return false;
            }
        }

        // add padding to a code block to make it easier to read
        public static bool AddCodeBlockPadding(CodeBlock cb, bool trailing, int padding = 1)
        {
            // if the section is not finalized, add padding to it
            if (cb.Finalized == false)
            {
                try
                {
                    // if the padding is trailing, add it to the end of the section
                    if (trailing)
                        cb.Trailing = padding;
                    // if the padding is not trailing, add it to the beginning of the section
                    else
                        cb.Padding = padding;
                }
                catch
                {
                    // if there is an error adding the padding to the section, print an error message
                    Console.WriteLine("Error adding padding to section");
                    return false;
                }
                return true;
            }
            else
            {
                // if the section is finalized, print an error message
                Console.WriteLine("Section has already been finalized 367");
                return false;
            }
        }

        public static Table CreateTable(string[] headers, int[] alignment, string[,] rows, string color = "Black", string font = "Arial")
        {
            // check if the headers and alignment arrays are the same length
            if (headers.Length != alignment.Length)
            {
                Console.WriteLine("Headers and alignment arrays must be the same length");
                return null!;
            }

            // check if the headers array is the same size as the rows array
            if (headers.Length != rows.GetLength(0))
            {
                Console.WriteLine("Headers array must be the same size as the rows array");
                return null!;
            }

            // create the table header
            TableHeader header = new()
            {
                Titles = headers,
                Alignment = alignment
            };

            // create the table rows
            TableRow[] tableRows = new TableRow[rows.GetLength(0)];
            for (int i = 0; i < rows.GetLength(0); i++)
            {
                // create a new TableRow object for each row
                tableRows[i] = new TableRow
                {
                    Entries = new string[rows.GetLength(1)]
                };
                // fill the entries of the row with the values from the rows array
                for (int j = 0; j < rows.GetLength(1); j++)
                {
                    tableRows[i].Entries[j] = rows[i, j];
                }
            }

            // write the user specified information to an instance of the Table object
            Table table = new()
            {
                TableHeader = header,
                TableRows = tableRows,
                Color = color,
                Font = font,
                Finalized = false
            };
            // return our new UL object
            return table;
        }

        // add a table to a section
        public static bool AddTable(Section section, Table table)
        {
            if (section == null)
            {
                // if the table is finalized, print an error message
                Console.WriteLine("Section is null");
                return false;
            }
            else if (section.Finalized)
            {
                // if the section is finalized, print an error message
                Console.WriteLine("Section has already been finalized");
                return false;
            }
            else if (table.Finalized)
            {
                // if the table is finalized, print an error message
                Console.WriteLine("Table has already been finalized");
                return false;
            }
            try
            {
                // create the header
                string fullTable = "| ";
                StringBuilder sbHeader = new(fullTable);
                // iterate through the headers and add them to the header string
                foreach (string h in table.TableHeader.Titles)
                {
                    sbHeader.Append($"{h} | ");
                }

                string alignment = "\n| ";
                StringBuilder sbAlignment = new(alignment);
                for (int i = 0; i < table.TableHeader.Alignment.Length; i++)
                {
                    switch (table.TableHeader.Alignment[i])
                    {
                        case 0: sbAlignment.Append(":--- | "); break;
                        case 1: sbAlignment.Append(":---: | "); break;
                        case 2: sbAlignment.Append("---: | "); break;
                        default: sbAlignment.Append("--- | "); break;
                    }
                }
                fullTable = sbHeader.ToString() + sbAlignment.ToString();

                // create the content of the table
                StringBuilder sbContent = new();
                foreach (TableRow row in table.TableRows)
                {
                    sbContent.Append("\n| ");
                    foreach (string entry in row.Entries)
                    {
                        string safeEntry = entry.Replace("|", "\\|");
                        sbContent.Append($" {entry.Trim()} |");
                    }
                }
                fullTable += sbContent.ToString();
                table.Finalized = true;
                section.Content = fullTable;
                return true;
            }
            catch
            {
                // if there is an error adding the table to the section, print an error message
                Console.WriteLine("Error adding table to section");
                return false;
            }
        }

        // write the MDFile object to a file
        public static bool WriteToFile(MDFile file)
        {
            try
            {
                // create a path that points to the desktop
                string path = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.Desktop), file.FileName);
                // indicate the file name and path so it can be found easily
                Console.WriteLine("Writing to: " + path);

                // create the file and write the information to it
                using (StreamWriter writer = new(path))
                {
                    // write the title of the file to the file
                    writer.WriteLine(file.Title);

                    // write each section to the file if they exist
                    if (file.Sections != null)
                    {
                        // write each section to the file
                        foreach (var section in file.Sections)
                        {
                            // write the title of the section to the file
                            writer.WriteLine(section.Title);
                            // write the content of the section to the file
                            writer.WriteLine(section.Content);
                        }
                    }
                }

                // indicate that we completed writing to the file
                Console.WriteLine("Write complete.");
                // return true to indicate the file was written successfully
                return true;
            }
            catch (Exception ex)
            {
                // if there is an error writing to the file, print an error message and the stack trace
                Console.WriteLine($"Error writing to file: {ex.Message}");
                Console.WriteLine(ex.StackTrace);

                // return false to indicate the file was not written successfully
                return false;
            }
        }

        // check that the file name does not contain any illegal characters
        private static bool IsFileNameValid(string fileName)
        {
            // Get all invalid characters for file names on the current OS
            char[] invalidChars = Path.GetInvalidFileNameChars();

            // Check if the file name contains any of the invalid characters
            return !fileName.Any(c => invalidChars.Contains(c));
        }

    }
    #endregion

    #region Section Classes
    // MDFile object
    public class MDFile
    {
        public required string FileName { get; set; }       // The name of the file to generate
        public required string Title { get; set; }          // The title of the document
        public List<Section>? Sections { get; set; }         // The sections to include in the document TODO:: add section object to allow font, color, and header defenition
        public string? DefaultFont { get; set; }            // The default font to use for the document unless a lower level section sets a different font
    }

    public interface IListElement
    {
        string[] Items { get; set; }
        string? Title { get; set; }
        string? Color { get; set; }
        string? Font { get; set; }
        int HeadingSize { get; set; }         // The size of the heading (1-6)
        bool BoldTitle { get; set; }         // Set to true if the title should be bold
    }
    public class UL : IListElement
    {
        public required string[] Items { get; set; }
        public string? Title { get; set; }
        public string? Color { get; set; }
        public string? Font { get; set; }
        public int HeadingSize { get; set; }
        public bool BoldTitle { get; set; }
    }

    public class OL : IListElement
    {
        public required string[] Items { get; set; }
        public string? Title { get; set; }
        public string? Color { get; set; }
        public string? Font { get; set; }
        public int HeadingSize { get; set; }
        public bool BoldTitle { get; set; }
    }

    // Section
    public class Section
    {
        public required string Title { get; set; }   // The title of the section
        public string? Color { get; set; }           // The color of the section
        public string? Font { get; set; }            // The font of the section
        public string? Content { get; set; }         // The content of the section
        public bool Finalized { get; set; }         // Set to true when the content of the section has been finalized
    }

    // Code Block
    public class CodeBlock
    {
        public required string Code { get; set; }
        public string? Lang { get; set; } // The language of the code block
        public string? Title { get; set; } // The title of the code block
        public string? Font { get; set; } // The font of the code block
        public string? Color { get; set; } // The color of the code block
        public bool Finalized { get; set; } // Set to true when the content of the code block has been finalized
        public int Padding { get; set; } // The padding of the code block
        public int Trailing { get; set; } // Set to true when the padding is trailing
    }

    // Table
    public class Table
    {
        public required TableHeader TableHeader { get; set; } // The header of the table
        public required TableRow[] TableRows { get; set; } // The rows of the table
        public string? Font { get; set; } // The font of the code block
        public string? Color { get; set; } // The color of the code block
        public bool Finalized { get; set; } // Set to true when the content of the code block has been finalized
        public int Padding { get; set; } // The padding of the code block
        public int Trailing { get; set; } // Set to true when the padding is trailing
    }

    // Table Header
    public class TableHeader
    {
        public required string[] Titles { get; set; } // The title of the header
        public required int[] Alignment { get; set; } // The alignment of the header (0 = left, 1 = center, 2 = right)
    }

    // Table Row
    public class TableRow
    {
        public required string[] Entries { get; set; } // The entries in the rows
    }
    #endregion
}