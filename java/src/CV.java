
import java.awt.image.BufferedImage;
import java.awt.image.DataBufferByte;
import org.opencv.core.Mat;
import org.opencv.core.*;
/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

/**
 *
 * @author Steven
 */
public class CV {
    
    public static Mat bufferedImageToMat(BufferedImage bi) {
        //System.out.println(bi.getType() + " " + BufferedImage.TYPE_BYTE_GRAY);
        Mat mat = new Mat(bi.getWidth(), bi.getHeight(), CvType.CV_8UC1);
        byte[] data = ((DataBufferByte) bi.getRaster().getDataBuffer()).getData();
        mat.put(0, 0, data);
        return mat;
    }

    public static BufferedImage matToBufferedImage(Mat matrix, BufferedImage bimg) {
        if ( matrix != null ) { 
            int cols = matrix.cols();  
            int rows = matrix.rows();  
            int elemSize = (int)matrix.elemSize();  
            byte[] data = new byte[cols * rows * elemSize];  
            int type;  
            matrix.get(0, 0, data);  
           // System.out.println("Channels: " + matrix.channels());
            switch (matrix.channels()) {  
            case 1:  
                type = BufferedImage.TYPE_BYTE_GRAY;  
                break;  
            case 3:  
                type = BufferedImage.TYPE_3BYTE_BGR;  
                // bgr to rgb  
                byte b;  
                for(int i=0; i<data.length; i=i+3) {  
                    b = data[i];  
                    data[i] = data[i+2];  
                    data[i+2] = b;  
                }  
                break;  
            default:  
                return null;  
            }  

            // Reuse existing BufferedImage if possible
            if (bimg == null || bimg.getWidth() != cols || bimg.getHeight() != rows || bimg.getType() != type) {
                bimg = new BufferedImage(cols, rows, type);
            }        
            bimg.getRaster().setDataElements(0, 0, cols, rows, data);
        } else { // mat was null
            bimg = null;
        }
        return bimg;  
    }   

}
