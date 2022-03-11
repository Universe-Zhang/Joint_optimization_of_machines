import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.lang.reflect.Field;
import java.text.DecimalFormat;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;





import org.apache.poi.hssf.usermodel.HSSFWorkbook;
import org.apache.poi.ss.usermodel.Sheet;
import org.apache.poi.ss.usermodel.Workbook;
import org.apache.poi.xssf.usermodel.XSSFWorkbook;

import ilog.concert.IloIntVar;
import ilog.concert.IloLinearNumExpr;
import ilog.cplex.IloCplex;

public class CommonCplexModel6 {

	//Logger logger = Logger.getLogger(CommonCplexModel6.class);

	/* Declarartion des varaibles */
	public int M = 3; // nb machines
	public int T = 5;// nb periods

	/*
	 * 
	 * range machines = 1..M; range periods = 1..T; range periods_T = 0..T;
	 * //range periods_T1 = 1..T-1; //range too=1..U;
	 */
	/*
	 * int machines = (int) (1 + Math.random() * (M - 1 + 1)); int periods =
	 * (int) (1 + Math.random() * (T - 1 + 1)); int periods_T = (int) (0 +
	 * Math.random() * (T - 0 + 1)); // int
	 * periods_T1=(int)(1+Math.random()*(T-1-1+1)); // int range
	 * too=(int)(1+Math.random()*(U-1+1));
	 */

	int machines = M;
	int periods = T;
	int periods_T = T;

	// Inputs values
	int a[];// a[machines]
	int b[];// b[machines]
	int h[];// h[periods]
	int d[];// d[periods]
	int p[];// p[periods]
	int c[];// c[periods]
	int s[];// s[periods]
	int cap[][];// cap[machines][periods]
	// int z[][];//z[machines][periods]

	private IloCplex model;
	private IloLinearNumExpr obj1;

	// Decisions variables
	private IloIntVar[][] x; // int x[machines][periods_T]
	private IloIntVar[][] Q; // int Q[machines][periods]
	private IloIntVar[] I; // int I[periods_T]
	private IloIntVar[] L;// int L[periods]

	private IloIntVar[][] Y; // boolean Y[machines][periods]
	private IloIntVar[][] z; // boolean z[machines][periods]

	public CommonCplexModel6(IloCplex _cplex) throws IOException {
		model = _cplex;

	}
	public void load_data(String filePath){
		InputStream is = null;
		/*
		 * let filePath
		 */
    	// filePath = "D:\\论文\\机器使用的联合优化算法\\Instances_LS\\Inst_1_5.xlsx";
    	Workbook wb = null;
        try {
            
            /** 调用本类提供的根据流读取的方法 */
            File file1 = new File(filePath);
            boolean isExcel2003 = true;
            if (WDWUtil.isExcel2007(filePath)) {
                isExcel2003 = false;
            }
            is = new FileInputStream(file1);
            if (isExcel2003) {
                wb = new HSSFWorkbook(is);
            } else {
                wb = new XSSFWorkbook(is);
            }
            is.close();
        } catch (Exception ex) {
            ex.printStackTrace();
        } finally {
            if (is != null) {
                try {
                    is.close();
                } catch (IOException e) {
                    is = null;
                    e.printStackTrace();
                }
            }
        }

    	 Sheet sheet = wb.getSheetAt(0);
        // List<List<String>> list = poi.read("d:/aaa.xls");
    	 int M = (int) sheet.getRow(1).getCell(0).getNumericCellValue();
    	 int T = (int) sheet.getRow(1).getCell(1).getNumericCellValue();
    	 int a[]=new int[M];
    	 int b[]=new int[M];
         System.out.println(M);
         System.out.println(T);
    	 for(int i = 1;i<1+M;i++){
    		 a[i-1]=(int) sheet.getRow(i).getCell(2).getNumericCellValue();
    		 b[i-1]=(int) sheet.getRow(i).getCell(3).getNumericCellValue();
    		 System.out.println(a[i-1]);
    		 System.out.println(b[i-1]);
    	 }
    	 int h[] = new int[T];
    	 int p[] = new int[T];
    	 int d[] = new int[T];
    	 int s[] = new int[T];
    	 int c[] = new int[T];
    	 for(int i = 1;i<1+T;i++){
    		 h[i-1]=(int) sheet.getRow(i).getCell(4).getNumericCellValue();
    		 p[i-1]=(int) sheet.getRow(i).getCell(5).getNumericCellValue();
    		 d[i-1]=(int) sheet.getRow(i).getCell(6).getNumericCellValue();
    		 s[i-1]=(int) sheet.getRow(i).getCell(7).getNumericCellValue();
    		 c[i-1]=(int) sheet.getRow(i).getCell(8).getNumericCellValue();
    		 System.out.println(h[i-1]);
    		 System.out.println(p[i-1]);
    		 System.out.println(d[i-1]);
    		 System.out.println(s[i-1]);
    		 System.out.println(c[i-1]);
    	 }
    	 int cap[][] = new int[M][T];
		 for(int m=1;m<1+T;m++){
			 for(int t=1;t<1+T;t++){

        		 cap[m-1][t-1]=(int) sheet.getRow(t).getCell(m).getNumericCellValue();
        	 }
    	 }
		

    
	}
	public void createModel(String filePath) {
	
//		int[] d = { 50, 30, 60, 70, 60 };
//		int[] h = { 2, 7, 3, 1, 2 };
//		int[] p = { 20, 100, 80, 30, 20 };
//		int[] c = { 3, 8, 2, 4, 6 };
//		int[][] cap = { { 500, 520, 510, 600, 500 },
//				{ 900, 800, 700, 650, 600 }, { 800, 900, 700, 550, 600 } };
//		int[] s = { 100, 500, 330, 400, 350 };
//		int[] a = { 20, 25, 25 };
//		int[] b = { 50, 40, 60 };
		
		InputStream is = null;
    	// filePath = "D:\\论文\\机器使用的联合优化算法\\Instances_LS\\Inst_1_5.xlsx";
    	Workbook wb = null;
        try {
            
            /** 调用本类提供的根据流读取的方法 */
            File file1 = new File(filePath);
            boolean isExcel2003 = true;
            if (WDWUtil.isExcel2007(filePath)) {
                isExcel2003 = false;
            }
            is = new FileInputStream(file1);
            if (isExcel2003) {
                wb = new HSSFWorkbook(is);
            } else {
                wb = new XSSFWorkbook(is);
            }
            is.close();
        } catch (Exception ex) {
            ex.printStackTrace();
        } finally {
            if (is != null) {
                try {
                    is.close();
                } catch (IOException e) {
                    is = null;
                    e.printStackTrace();
                }
            }
        }

    	 Sheet sheet = wb.getSheetAt(0);
        // List<List<String>> list = poi.read("d:/aaa.xls");
    	 int M = (int) sheet.getRow(1).getCell(0).getNumericCellValue();
    	 int T = (int) sheet.getRow(1).getCell(1).getNumericCellValue();
    	 int a[]=new int[M];
    	 int b[]=new int[M];
//         System.out.println(M);
//         System.out.println(T);
    	 for(int i = 1;i<1+M;i++){
    		 a[i-1]=(int) sheet.getRow(i).getCell(2).getNumericCellValue();
    		 b[i-1]=(int) sheet.getRow(i).getCell(3).getNumericCellValue();
//    		 System.out.println(a[i-1]);
//    		 System.out.println(b[i-1]);
    	 }
    	 int h[] = new int[T];
    	 int p[] = new int[T];
    	 int d[] = new int[T];
    	 int s[] = new int[T];
    	 int c[] = new int[T];
    	 for(int i = 1;i<1+T;i++){
    		 h[i-1]=(int) sheet.getRow(i).getCell(4).getNumericCellValue();
    		 p[i-1]=(int) sheet.getRow(i).getCell(5).getNumericCellValue();
    		 d[i-1]=(int) sheet.getRow(i).getCell(6).getNumericCellValue();
    		 s[i-1]=(int) sheet.getRow(i).getCell(7).getNumericCellValue();
    		 c[i-1]=(int) sheet.getRow(i).getCell(8).getNumericCellValue();
//    		 System.out.println(h[i-1]);
//    		 System.out.println(p[i-1]);
//    		 System.out.println(d[i-1]);
//    		 System.out.println(s[i-1]);
//    		 System.out.println(c[i-1]);
    	 }
    	 int cap[][] = new int[M][T];
		 for(int m=9;m<9+M;m++){
			 for(int t=1;t<1+T;t++){

        		 cap[m-9][t-1]=(int) sheet.getRow(t).getCell(m).getNumericCellValue();
        	 }
    	 }
		
		machines = M;
		periods = T;
		periods_T = T;
		

		try {
			obj1 = model.linearNumExpr();
			x = new IloIntVar[machines][periods_T];
			Q = new IloIntVar[machines][periods];
			I = new IloIntVar[periods_T];
			L = new IloIntVar[periods];
			Y = new IloIntVar[machines][periods];
			z = new IloIntVar[machines][periods];

			for (int i = 0; i < machines; i++) {
				for (int t = 0; t < periods; t++) {
					x[i][t] = model.intVar(0, Integer.MAX_VALUE, "x_" + i + "_"
							+ t);
					z[i][t] = model.intVar(0, 2, "z_" + i + "_" + t);
					obj1.addTerm(a[i], x[i][t]);
					obj1.addTerm(b[i], z[i][t]);
				}
			}
			for (int t = 0; t < periods; t++) {
				for (int i = 0; i < machines; i++) {
					Y[i][t] = model.intVar(0, 2, "Y_" + i + "_" + t);
					Q[i][t] = model.intVar(0, Integer.MAX_VALUE, "Q_" + i + "_"
							+ t);
					I[t] = model.intVar(0, Integer.MAX_VALUE, "I_" + t);
					L[t] = model.intVar(0, Integer.MAX_VALUE, "L_" + t);
					obj1.addTerm(s[t], Y[i][t]);
					obj1.addTerm(c[t], Q[i][t]);
					obj1.addTerm(h[t], I[t]);
					obj1.addTerm(p[t], L[t]);
				}
			}

			for (int t = 1; t < periods; t++) {

				IloLinearNumExpr constr1 = model.linearNumExpr();

				for (int i = 0; i < machines; i++) {
					constr1.addTerm(1, Q[i][t]);
				}

				constr1.addTerm(-1, I[t]);
				constr1.addTerm(1, I[t - 1]);
				constr1.addTerm(1, L[t]);
				model.addEq(constr1, d[t],
						"I[t]== (sum (i in machines) Q[i][t])+ I[t-1] + L[t] - d[t]");
			}
			
			IloLinearNumExpr constr1 = model.linearNumExpr();

			for (int i = 0; i < machines; i++) {
				constr1.addTerm(1, Q[i][0]);
			}

			constr1.addTerm(-1, I[0]);
			constr1.addTerm(1, L[0]);
			model.addEq(constr1, d[0],
					"I[0]== (sum (i in machines) Q[i][0])+ L[t] - d[t]");
			

			//model.addEq(0, I[0], "I[0]==0");

			for (int t = 0; t < periods; t++) {
				for (int i = 0; i < machines; i++) {
					IloLinearNumExpr constr2 = model.linearNumExpr();
					constr2.addTerm(1, Y[i][t]);
					constr2.addTerm(1, z[i][t]);
					model.addLe(constr2, 1, "Y[i][t]<= (1-z[i][t])");
					IloLinearNumExpr constr3 = model.linearNumExpr();
					constr3.addTerm(1000, Y[i][t]);
					model.addLe(Q[i][t], constr3, "Q[i][t]<= 10000*Y[i][t]");
				}
			}

			for (int i = 0; i < machines; i++) {
				for (int t = 0; t < periods; t++) {
					model.addLe(Q[i][t], cap[i][t], "Q[i][t]<= cap[i][t]");
				}
			}

			for (int t = 0; t < periods; t++) {
				model.addLe(L[t], d[t], "L[t]<= d[t]");
			}

			for (int i = 0; i < machines; i++) {
				for (int t = 1; t < periods; t++) {
					IloLinearNumExpr constr4 = model.linearNumExpr();
					constr4.addTerm(1, x[i][t]);
					constr4.addTerm(-1, x[i][t - 1]);
					constr4.addTerm(-1, Y[i][t]);
					constr4.addTerm(100000, z[i][t]);
					model.addGe(constr4,0,
							"x[i][t] >= x[i][t-1]+Y[i][t]-(1000*z[i][t])]");
				}
			}
			
			for (int i = 0; i < machines; i++) {
					IloLinearNumExpr constr4 = model.linearNumExpr();
					constr4.addTerm(1, x[i][0]);
					constr4.addTerm(-1, Y[i][0]);
					constr4.addTerm(100000, z[i][0]);
					model.addGe(constr4,0,
							"x[i][t] >= Y[i][t]-(1000*z[i][t])]");
			}

			for (int i = 0; i < machines; i++) {
				IloLinearNumExpr constr5 = model.linearNumExpr();
				for (int t = 0; t < periods; t++) {
					constr5.addTerm(1, z[i][t]);
				}
				model.addGe(constr5, 1, "z[i][t]>= 1");
			}

			

			for (int i = 0; i < machines; i++) {
				for (int t = 0; t < periods; t++) {
					model.addGe(x[i][t], 0, "x[i][t] >=0");
				}
			}

			for (int t = 0; t < periods; t++) {
				model.addGe(I[t], 0, "I[t] >=0");
				model.addGe(L[t], 0, "L[t] >=0");
				for (int i = 0; i < machines; i++) {
					model.addGe(Q[i][t], 0, "Q[i][t] >=0");
				}
			}


			model.addMinimize(obj1);
		} catch (Exception e) {
			e.printStackTrace();
		}

	}

	public static void main(String[] args) {

		long startTime1 = System.currentTimeMillis(); 
		// String name1 = "Inst_10_";
		int name1[] = {1,3,5,10};
		int name2[] = {5,10,15,30,60,80,100};
		for (int n1 : name1){
			for (int n2 : name2) {
				/*
				 * let filePath be the location of data file  
				 * 在此处更改文件路径
				 * 
				 */
				
					
				String filePath = "..\\data\\Instances_LS\\Inst_"+n1+"_"+n2+".xlsx";
		
				try {
		
		
					IloCplex _cplex = new IloCplex();
					CommonCplexModel6 model = new CommonCplexModel6(_cplex);
					model.createModel(filePath);
					// _cplex.exportModel("modelflow/modelflow"+count+".lp");
					System.out.println(filePath);
					if (_cplex.solve()) {
						// model.print(_cplex);
						double objVal = _cplex.getObjValue();
						System.out.println("objective value: " + objVal);
						_cplex.end();
		
					} else {
		
						_cplex.end();
						System.out
								.println("\n~~~~~~~~~~~~~~~~~~~~~~~~异常结束~~~~~~~~~~~~~~~~~~~~~~~~~");
					}
		
					// model.print(_cplex);
				} catch (Exception e) {
					e.printStackTrace();
		
				}
				long endTime1 = System.currentTimeMillis(); 
				System.out
						.println("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~");
				System.out.println("                                     结束"
						+ (endTime1 - startTime1)  + "ms                  ");
			}
		}
	}

	public void print(IloCplex _cplex) throws Exception {
		for (int i = 0; i < machines; i++) {
			for (int t = 0; t < periods; t++) {
				if (getX()[i][t] != null&&  _cplex.getValue(getX()[i][t])>0) {
					System.out.println( "x_" + i + "_" + t + " "
							+ _cplex.getValue(getX()[i][t]));
				}
				if (getQ()[i][t] != null && _cplex.getValue(getQ()[i][t])>0) {
					System.out.println( "Q_" + i + "_" + t + " "
							+ _cplex.getValue(getQ()[i][t]));
				}
				if (getY()[i][t] != null && _cplex.getValue(getY()[i][t])>0) {
					System.out.println( "Y_" + i + "_" + t + " "
							+ _cplex.getValue(getY()[i][t]));
				}
				if (getZ()[i][t] != null && _cplex.getValue(getZ()[i][t])>0) {
					System.out.println( "z_" + i + "_" + t + " "
							+ _cplex.getValue(getZ()[i][t]));
				}
			}
		}
		for (int t = 0; t < periods; t++) {
			if (getI()[t] != null && _cplex.getValue(getI()[t])>0) {
				System.out.println( "I_" + t + " "
						+ _cplex.getValue(getI()[t]));
			}
			if (getL()[t] != null && _cplex.getValue(getL()[t])>0) {
				System.out.println( "L_"  + t + " "
						+ _cplex.getValue(getL()[t]));
			}
		}
		double minCost = _cplex.getObjValue();

		String result = "\n\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~鐟滅増鎸告晶鐘垫喆閿濆洦鐣遍柡鍫嫹閻剟骞嬮幇顓熸嫳闁挎稑鐗忓ú浼村冀閸パ冩瘣闁轰焦婢橀敓浠嬫晬婢у瘡~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n";

		result += "\t\t\t\t" + minCost + "\n\n\n";
		//logger.info(result);
	}

	// getter

	public IloLinearNumExpr getObj1() {
		return obj1;
	}

	public void setObj1(IloLinearNumExpr obj1) {
		this.obj1 = obj1;
	}

	public IloIntVar[][] getX() {
		return x;
	}

	public void setX(IloIntVar[][] x) {
		this.x = x;
	}

	public IloIntVar[][] getQ() {
		return Q;
	}

	public void setQ(IloIntVar[][] q) {
		Q = q;
	}

	public IloIntVar[] getI() {
		return I;
	}

	public void setI(IloIntVar[] i) {
		I = i;
	}

	public IloIntVar[] getL() {
		return L;
	}

	public void setL(IloIntVar[] l) {
		L = l;
	}

	public IloIntVar[][] getY() {
		return Y;
	}

	public void setY(IloIntVar[][] y) {
		Y = y;
	}

	public IloIntVar[][] getZ() {
		return z;
	}

	public void setZ(IloIntVar[][] z) {
		this.z = z;
	}

	
	public IloCplex getModel() {
		return model;
	}

	public void setModel(IloCplex model) {
		this.model = model;
	}

}
