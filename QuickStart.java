import java.util.Arrays;
import java.util.Scanner;
public class QuickStart
{
    public static void main(String[] args) 
    {
        Scanner ce = new Scanner(System.in);
        System.out.println("Data points? :");
        int amount = ce.nextInt();
        String myArray[] = new String[amount];
        System.out.println("enter element");
        for (int i = 0; i < amount; i++) 
        {
            myArray[i] = ce.next();
        }
        System.out.println(Arrays.toString(myArray));
        ce.close();
    }
}