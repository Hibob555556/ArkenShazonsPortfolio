namespace stepcombination
{
    public class stepcombination
    {
        public static void Main(string[] args)
        {
            const int stepCount = 5;
        }

        public static int stepCombonation(int steps)
        {
            int count = 0;
            int[] options = { 1, 2 };
            int possibleCombinations = steps
            for (int i = 0; i < steps; i++)
            {
                // handle first iteration
                if (i == 0) // will always be 1, 1, 1, 1...
                {
                    count = steps;
                }
                // handle the last iteration
                else if (i == steps - 1) // will always be 2, 2, 2, 2...
                {
                    // if steps is divisible by 2 we can very quickly calcualte the number of steps needed
                    if (steps % 2 == 0)
                        count = steps / 2;
                    else
                    {
                        count = -1;
                    }
                }

            }
        }
    }
}