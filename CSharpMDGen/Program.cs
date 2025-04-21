using System.Text;

namespace CSharpMDGen
{
    public class Program
    {
        public static void Main(string[] args)
        {
            #region Demo
            // create our MDFile object
            MDFile file = MDGen.Create();

            // create sections
            var intro = MDGen.CreateSection("Introduction", "This is the introduction section", "Arial", "Black");
            var gettingStarted = MDGen.CreateSection("Getting Started", "This is the getting started section", "Arial", "Black");
            var advanced = MDGen.CreateSection("Advanced Topics", "This is the advanced topics section", "Arial", "Black");

            // create a code block
            string code = "Console.WriteLine(\"Hello World!\");";
            var codeBlock = MDGen.CreateCodeBlock(code, "csharp", "Hello World Example");
       
            // add padding to the code block to make it easier to read
            MDGen.AddCodeBlockPadding(codeBlock, false, 1);

            // add the code block to the intro section
            MDGen.AddCodeBlock(intro, codeBlock);

            // create an unordered list
            string[] items = { "Item 1", "Item 2", "Item 3" };
            var ul = MDGen.CreateUL(items, "Unordered List");

            // add our unordered list to the gettingStarted section
            MDGen.AddUL(gettingStarted, ul);

            // create an ordered list
            string[] items2 = { "Item 1", "Item 2", "Item 3" };
            var ol = MDGen.CreateOL(items2, "Ordered List");

            // add our ordered list to the advanced section
            MDGen.AddOL(advanced, ol);

            // add padding to the end of each section to make it easier to read
            MDGen.AddSectionPadding(intro, false, 1);
            MDGen.AddSectionPadding(intro, true, 2);
            MDGen.AddSectionPadding(gettingStarted, true, 2);

            // add sections to file
            MDGen.AddSection(file, intro);
            MDGen.AddSection(file, gettingStarted);
            MDGen.AddSection(file, advanced);

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
        public static UL CreateUL(string[] items, string title = null!, string color = "Black", string font = "Arial")
        {
            // write the user specified information to an instance of the UL object
            UL ul = new()
            {
                Items = items,
                Title = title,
                Color = color,
                Font = font
            };
            // return our new UL object
            return ul;
        }

        // create an ordered list object
        public static OL CreateOL(string[] items, string title = null!, string color = "Black", string font = "Arial")
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
        public static bool AddUL(Section section, UL ul, bool smallTab = true)
        {
            // define tab sizes (4 spaces and 2 spaces)
            const String TAB = "    ";
            const String SMALL_TAB = "  ";

            // if the section is not finalized, add the unordered list to it
            if (section.Finalized == false)
            {
                try
                {
                    // add the title of the unordered list to the section
                    section.Content += $"\n{ul.Title}\n";

                    // add the items in the unordered list to the section with the selected tab size
                    StringBuilder sb = new(section.Content);
                    foreach (var item in ul.Items)
                    {
                        if (smallTab)
                            sb.AppendLine($"{SMALL_TAB}- {item}\n");
                        else
                            sb.AppendLine($"{TAB}- {item}\n");
                    }
                    section.Content = sb.ToString();
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

        // add an ordered list to a section
        public static bool AddOL(Section section, OL ol, bool smallTab = true)
        {
            // define tab sizes (4 spaces and 2 spaces)
            const String TAB = "    ";
            const String SMALL_TAB = "  ";

            // if the section is not finalized, add the unordered list to it
            if (section.Finalized == false)
            {
                try
                {
                    // add the title of the unordered list to the section
                    section.Content += $"\n{ol.Title}\n";

                    // add the items in the unordered list to the section with the selected tab size
                    StringBuilder sb = new(section.Content);
                    int index = 1;
                    foreach (var item in ol.Items)
                    {
                        if (smallTab)
                            sb.AppendLine($"{SMALL_TAB}{index}. {item}\n");
                        else
                            sb.AppendLine($"{TAB}{index}. {item}\n");
                        index++;
                    }
                    section.Content = sb.ToString();
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
                Console.WriteLine("Section has already been finalized 261");
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
                            section.Content = section.Content + "\n";
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
                            sb.AppendLine("\n");
                        sb.AppendLine($"\n***{codeBlock.Title}***");
                    }

                    if (!string.IsNullOrWhiteSpace(codeBlock.Lang))
                        sb.AppendLine($"```{codeBlock.Lang}");
                    else
                        sb.AppendLine("```");

                    sb.AppendLine(codeBlock.Code.Trim());
                    sb.AppendLine("```");

                    for (int i = 0; i < codeBlock.Trailing; i++)
                        sb.AppendLine("\n");

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
                using (StreamWriter writer = new StreamWriter(path))
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

    // Unordered list
    public class  UL
    {
        public required string[] Items { get; set; } // The items in the list
        public string? Title { get; set; }           // The title of the list this will not be required in case they want to add their own formatting for the title
        public string? Color { get; set; }           // The color of the items in the list
        public string? Font { get; set; }            // The font of the items in the list

    }

    // Ordered list
    public class OL
    {
        public required string[] Items { get; set; } // The items in the list
        public string? Title { get; set; }           // The title of the list this will not be required in case they want to add their own formatting for the title
        public string? Color { get; set; }           // The color of the items in the list
        public string? Font { get; set; }            // The font of the items in the list
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
    #endregion
}