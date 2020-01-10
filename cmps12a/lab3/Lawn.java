//Lawn.java
//Andrew Nguyen
//anguy224 
//lab3
//calculates are of lawn to be mowed and how long it would take

import java.util.Scanner;

public class Lawn
{
   public static void main (String[] args)
   {
      Scanner inputText = new Scanner(System.in);
      
      double lotLength = inputText.nextDouble();
      double lotWidth = inputText.nextDouble();
      double lotArea = lotLength*lotWidth;
             
      double houseLength = inputText.nextDouble();
      double houseWidth = inputText.nextDouble();
      double houseArea = houseLength*houseWidth;
      
      double lawnArea = lotArea-houseArea;
      System.out.println("The lawn area is " + lawnArea + " square feet.");
      
      double mowRate = inputText.nextDouble();
      
      
      double time = lawnArea/mowRate;
      int hours, minutes, seconds;
      
      seconds = (int) Math.round(time);
      minutes = seconds/60;
      seconds = seconds%60;
      hours = minutes/60;
      minutes = minutes%60;
      
      System.out.println("The mowing time is " + hours + " hour"+(hours==1?" ":"s ") + minutes + " minute"+(minutes==1?" ":"s ") + seconds + " second"+(seconds==1?".":"s."));
   }
}

