import java.io.BufferedReader;
import java.io.FileReader;

import javax.security.auth.kerberos.KerberosKey;

/**
     The following class SGD shows a method called SGD(i.e Stochastic Gradient Descent)that find all coefficients for liner regression h(x) = a0 +a1*x1 + a2*x2 + a3*x3 +..... 
     Before finding the coefficients, the function normalizeMatrix(double[][] inputMatrix)scale the features(i.e X)so that their magnitudes are similar( I normalize each feature to have mean zero and variance 1)
**/
public class SGD_linearRegression
{
	public static void main(String[] args) throws Exception 
	{
		double[][] temp = inputDataToMatrix("linear_regression.txt",50,2);
		
		
		normalizeMatrix(temp);
		double[] theda = new double[2]; 
		
		
		double learningRate = 0.05;
		 	for(int k = 0;k<=50;k++) {
		 		
				for(int i = 0;i < temp.length;i++)
					
				{
					//learningRate -= 0.05/500;  
					double h = theda[0];
					for(int j = 0;j < (theda.length-1);j++)
					{
						h += theda[j+1] * temp[i][j];
					}
					theda[0] += learningRate * (temp[i][1] - h);
					theda[1] += learningRate * (temp[i][1] - h) * temp[i][0];
					//theda[2] += learningRate * (temp[i][2] - h) * temp[i][1];
					/**if((i+1)%10 == 0) 
					{
						System.out.println(theda[0] + "," + theda[1] + "," + theda[2]);
						double jtheda=0;  
						for(int s = 0;s < temp.length;s++)
						{
							jtheda += Math.pow((theda[0] + theda[1] * temp[s][0] + theda[2] * temp[s][1]-temp[s][2]), 2);
						}
						System.out.println(jtheda/1000);
						
				     }**/	
					
				}
				double jtheda=0;  
				for(int s = 0;s < temp.length;s++)
				{
					
					jtheda += Math.pow((theda[0] + theda[1] * temp[s][0] -temp[s][1]), 2);
				}
				System.out.println(theda[0] + "," + theda[1] + "," );
				System.out.println(jtheda/1000);
				System.out.println("\t");
			}
			
	}
	
	
	/*
	 * read the data
	 */
	public static double[][] inputDataToMatrix(String dataFileName, int row, int col)
	{
		String[][] dataMatrix = new String[row][col];
		double[][] inputDataToMatrix = new double[row][col];
		
		try 
		{ 
            BufferedReader reader = new BufferedReader(new FileReader(dataFileName));
            //reader.readLine();
            reader.readLine();
            String line = null;
            int i = 0;
            while((line=reader.readLine())!=null)
            { 
            	String[] item = line.split(",");
            	for(int j = 0;j < col;j++)
            	{
	                dataMatrix[i][j] = item[j];
	                inputDataToMatrix[i][j] = Double.parseDouble(dataMatrix[i][j].trim());   
            	}
            	i++;
            } 
            reader.close(); 
        } 
		catch (Exception e) 
		{ 
            e.printStackTrace(); 
        }
		
		return inputDataToMatrix;
				
	}
	
	/*
	 * Nomalize the data
	 */
	public static double[][] normalizeMatrix(double[][] inputMatrix) 
	{
		double[] sumOfFeature = new double[inputMatrix[0].length];
		double[] expOfFeature = new double[inputMatrix[0].length];
		double[] sumOfPow = new double[inputMatrix[0].length];
		double[] varOfFeature = new double[inputMatrix[0].length];
		
		for(int j = 0;j < inputMatrix[0].length;j++) 
		{
			for(int i = 0;i < inputMatrix.length;i++)
			{
				sumOfFeature[j] += inputMatrix[i][j];
			}
		
			expOfFeature[j] = sumOfFeature[j]/inputMatrix.length;
			for(int k = 0;k < inputMatrix.length;k++) 
			{
				inputMatrix[k][j] -= expOfFeature[j];
				sumOfPow[j] += Math.pow(inputMatrix[k][j], 2);
			}
			varOfFeature[j] = Math.sqrt(sumOfPow[j]/inputMatrix.length);
			for(int m = 0;m < inputMatrix.length;m++) 
			{
				inputMatrix[m][j] /= varOfFeature[j];
			}
		}
		
		return inputMatrix;
		
	}
	
}

