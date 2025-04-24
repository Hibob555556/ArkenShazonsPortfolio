using Microsoft.CodeAnalysis;
using Microsoft.CodeAnalysis.CSharp;
using Microsoft.CodeAnalysis.CSharp.Syntax;

namespace CSharpMDGen
{
    class CSharpMDGen
    {
        public static void Main()
        {
            // set the current directory to the one containing the file
            Directory.SetCurrentDirectory("../../../");

            string fileName = "sampleProg.cs";

            // read in the csharp file
            StreamReader reader = new($"./{fileName}");
            string file = reader.ReadToEnd();
            reader.Close();

            // get the tree of the file
            string className;
            List<string> methodNames = [];
            List<string> constructorNames = [];
            List<Tuple<string, List<string>, List<string>>> classToMethods = []; // class, method, constructor
            SyntaxTree tree = CSharpSyntaxTree.ParseText(file);

            foreach (var classNode in tree.GetRoot().DescendantNodes().OfType<ClassDeclarationSyntax>())
            {
                className = classNode.Identifier.Text;

                // Get all method declarations within this class
                foreach (var method in classNode.Members.OfType<MethodDeclarationSyntax>())
                {
                    methodNames.Add(method.Identifier.Text);
                }

                foreach (var constructor in classNode.Members.OfType<ConstructorDeclarationSyntax>())
                {
                    constructorNames.Add(constructor.Identifier.Text);
                }

                classToMethods.Add(new Tuple<string, List<string>, List<string>>(className, [.. methodNames], [.. constructorNames]));
                methodNames.Clear();
                constructorNames.Clear();
            }

            // create a list of class names
            List<string> names = [];
            foreach (var tpl in classToMethods)
                names.Add(tpl.Item1);

            // create a markdown file
            MDFile mdFile = MDGen.Create("CodeDocumentation", "Inventory System Documentation");

            // create an introduction section
            Section intro = MDGen.CreateSection("Introduction", $"- This file contains the documentation for the Inventory System file `{fileName}`.", "Arial");

            // create an ordered list of classes
            List<string> styleizedNames = [];
            foreach (var name in names)
                styleizedNames.Add($"`{name}`");
            OL methods = MDGen.CreateOL([.. styleizedNames], "Classes:");
            MDGen.AddListElement(intro, methods, ordered: true);
            MDGen.AddSection(mdFile, intro);

            // create sections
            List<Section> sections = [];
            foreach (var name in names)
                sections.Add(MDGen.CreateSection(name, $"- The following methods are contained within the `{name}` class:", "Arial"));

            // populate each section
            foreach (var section in sections.ToArray())
            {
                List<string> classMethods = [];
                List<string> classConstructors = [];
                string cn = section.Title.Replace("## ", "").Trim();
                foreach (var sec in classToMethods)
                {
                    if (sec.Item1 == cn)
                    {
                        foreach (var method in sec.Item2)
                        {
                            if (sec.Item1 == cn)
                                classMethods.Add($"`{method}`");
                        }
                        foreach (var constructor in sec.Item3)
                        {
                            if (sec.Item1 == cn)
                                classConstructors.Add($"`{constructor}`");
                        }
                    }
                }

                // create lists from the methods and constructors
                UL l = MDGen.CreateUL([.. classMethods.ToArray()], "Methods:", headingSize: 5);
                UL l2 = MDGen.CreateUL([.. classConstructors.ToArray()], "Constructors:", headingSize: 5);

                // add the lists to a section
                if (classMethods.Count > 0)
                    MDGen.AddListElement(section, l, ordered: false, padBottom: true);

                if (classConstructors.Count > 0)
                {
                    Text text = MDGen.CreateText($"The following constructors are contained within the `{cn}` class:");
                    MDGen.AddText(section, text, bullet: true);
                    MDGen.AddListElement(
                        section, 
                        l2, 
                        ordered: false, 
                        smallTab: false, 
                        padTitle: true, 
                        padBottom: true
                    );
                }
                MDGen.AddSection(mdFile, section);
            }

            // write the file to disk
            MDGen.WriteToFile(mdFile);
        }
    }
}

