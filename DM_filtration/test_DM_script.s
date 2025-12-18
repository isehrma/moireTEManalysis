
//////////////////////////////////////////////////////////////////
//Adjust the start and end angles and radiuses
//Choose them by looking at FFT and filtrated image
//Are all moire you wish to include visible at filtered image?
//Is there a lot of noise, too big/small angles/radiuses

//Angles should be typed in radians

Number startAngle = 40*3.1415/180;
Number endAngle = 60*3.1415/180;
Number startRadius = 30;
Number endRadius = 90;

///////////////////////////////////////////////////////////////////

//Don't change those values

Number numCircularMasks = 1;
Number numAngularMasks = 1;

Number pi = 3.141592653589793238462643383279502884197169399375105820974944592307816406286208998628034825342117067982148086513282306647093844609550582231725359408128481117450284102701938521105559644622948954930381964428

// Function to create angular masks and slice them into user-defined pieces
void CreateAndSliceAngularMasks(complexImage img, Number startAngle, Number endAngle, Number numPieces, string baseName) {
    Number width = img.ImageGetDimensionSize(0);
    Number height = img.ImageGetDimensionSize(1);
    Number centerX = width / 2;
    Number centerY = height / 2;
    Number angleStep = (endAngle - startAngle) / numPieces;
    

    for (Number i = 0; i < numPieces; i++) {
        Number startMaskAngle = (startAngle + i * angleStep);
        Number endMaskAngle = (startAngle + (i + 1) * angleStep);
        Number startMaskAngle2 = startMaskAngle + 60*pi/180;
        Number startMaskAngle3 = startMaskAngle + 120*pi/180;
        Number endMaskAngle2 = endMaskAngle + 60*pi/180;
        Number endMaskAngle3 = endMaskAngle + 120*pi/180;

        // Create angular mask
        Image mask := RealImage("Mask", 4, width, height);
        mask = 0;
        AddWedgeMaskToImage(mask, centerX, centerY, cos(startMaskAngle), sin(startMaskAngle), cos(endMaskAngle), sin(endMaskAngle), 1, 0);
		AddWedgeMaskToImage(mask, centerX, centerY, cos(startMaskAngle2), sin(startMaskAngle2), cos(endMaskAngle2), sin(endMaskAngle2), 1, 0);
		AddWedgeMaskToImage(mask, centerX, centerY, cos(startMaskAngle3), sin(startMaskAngle3), cos(endMaskAngle3), sin(endMaskAngle3), 1, 0);
		

         // Apply mask to original image
        complexImage maskedImg := img * mask;
        converttopackedcomplex(maskedImg)
        
        string maskname = "FFT_of_" +baseName + ".png";
        maskedImg.ShowImage();
        ImageSetName(maskedImg,maskname)

        // Perform IFFT to revert back to space domain
        Image originalSpaceImg := packedifft(maskedImg);
		
		 // Save the reverted image
        string filename = baseName;
        
        ShowImage(originalSpaceImg)
        
        //Save(originalSpaceImg)
        
        ImageSetName(originalSpaceImg,filename)
        
        
        
    }
}

// Function to create circular masks 
void CreateAndSliceCircularMasks(complexImage img, Number startRadius, Number endRadius, Number numPieces, string baseName) {
    Number width = img.ImageGetDimensionSize(0);
    Number height = img.ImageGetDimensionSize(1);
    Number centerX = width / 2;
    Number centerY = height / 2;
    Number radiusStep = (endRadius - startRadius) / numPieces;

    for (Number i = 0; i < numPieces; i++) {
        Number innerRadius = startRadius + i * radiusStep;
        Number outerRadius = startRadius + (i + 1) * radiusStep;
        Number filter_size = 1
        Number do_inverse = 0 // Here internet says Boolean should be

        // Create circular mask
        Image mask := RealImage("Mask", 4, width, height);
		mask=0
        //mask.ShowImage();
        AddBandPassMaskToImage(mask, centerX, centerY, innerRadius, outerRadius, filter_size, do_inverse);

        // Apply mask to original image
        complexImage maskedImg := img * mask;
        converttopackedcomplex(maskedImg)
        //maskedImg.ShowImage();

        // Perform IFFT to revert back to space domain
        //Image originalSpaceImg := packedifft(maskedImg);

        // Save the reverted image
        string revertedImgName = baseName + "_" + i;
        
        //ShowImage(originalSpaceImg)
        //compleximage fftimg = packedfft(originalSpaceImg)
        //ImageSetName(originalSpaceImg,revertedImgName)
        
        
        
        
        // Create and slice angular masks
        CreateAndSliceAngularMasks(maskedImg, startAngle, endAngle, numAngularMasks, revertedImgName);
       
        
    }
}


// Main function
void Main() {
    // Get currently active image from workspace
    Image img := GetFrontImage();
    if (img.ImageIsValid()) {
        string baseName = img.ImageGetName();

        // Perform FFT on the image
        compleximage fftImg := packedfft(img);

        // Display FFT image
        //fftImg.ShowImage();

        // Get user-defined parameters for circular masks
        
        

         
        //Create masks
        CreateAndSliceCircularMasks(fftImg, startRadius, endRadius, numCircularMasks, baseName);
        
        
    } else {
        OKDialog("No valid image found in the workspace!");
    }
}

// Call main function
Main();
