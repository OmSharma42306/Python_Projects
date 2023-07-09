import os
import win32com.client as say
speaker=say.Dispatch("SAPI.SpVoice")
print("******************************* Welcome to My Attendence System ********************************")
speaker.speak("Hello Everyone ! Welcome to My Admission System")
while True:
    print("1--> New Student Admission\n2--> Display All\n3-->Search Student\n4-->Edit or Update Record\n5-->Delete Student Record\n6-->Coursewise List\n7-->No.of Admissions According to Course\n8-->Exit..")
    speaker.speak("Enter Your Choice :")
    choice=int(input("Enter Your Choice : "))
    if choice==1:    
        speaker.speak("Enter Your U U C M S Number")
        uucms_no=input("Enter UUCMS No : ")
        speaker.speak("Enter Your Name")
        name=input("Enter Name : ")
        speaker.speak("Enter Your Gender            if male type 'm' or Female type 'f'")
        gender=input("Enter Gender --> if Male type 'm' or Female type 'f' : ")
        if gender=='m':
            gender="Male"
        elif gender=='f':
            gender="Female"
        speaker.speak("Avilable Courses !")
        print("Avilable Courses ! \n 1.BCA\n2.BBA\n3.B.sc\n4.B.com\n5.BA")
        speaker.speak("Enter Your Course according to Number Format")
        course=int(input("Enter in Number : "))
        if course==1:
            course="BCA"
        elif course==2:
            course="BBA"
        elif course==3:
            course="B.sc"
        elif course==4:
            course="B.com"
        elif course==5:
            course="BA"
        speaker.speak("Enter Your Sem")
        sem=input("Enter Sem : ")
        speaker.speak("Enter Your Fees")
        fees=input("Enter Fees : ") 
        
        s=uucms_no+","+name+","+gender+","+course+","+sem+","+fees+","
        
        f=open("students.csv","a")
        a=f.write(f"{s}")
        a=f.write('\n')
        f.close()
        print("*************************************************************************")
        speaker.speak("Data Saved Successfully !")
        print("Data Saved Successfully !")
        print("*************************************************************************")

    elif choice==2:
        f=open("students.csv","r")
        a=f.read()   
        z=a.replace(',',"\t")
        print("UUCMS   Name           Gender  Course   Sem     Fees")
        print(z)
        f.close()
    # SIR DD CODE
    # f=open("students.csv","r")
    # data=f.read()
    # lines=data.split("\n")
    # lines=lines[0:len(lines)-1]   
    # 
    # print("UUCMSNO\tName\tGender\tCourse\tSem\tFees")
    # for l in lines:
    #     s=l.split(",")
    #     print(f"{s[0]}\t{s[1]}\t{s[2]}\t{s[3]}\t{s[4]}\t{s[5]}")
    # f.close()
    # print(lines)

    elif choice==3:
        f=open("students.csv","r")
        s=f.read()
        b=s.replace("\n","")
        
        all_details_list=b.split(",")
        
        all_lists=[]
        i=0
        l=len(all_details_list)
        while i<l-1:
            j=i+6
            z=all_details_list[i:j]
            all_lists.append(z)
            i=i+6
            f.close()
        speaker.speak("Enter Your U U C M S Number")
        uucms_no=input("Enter UUCMS NO :")
        for item in all_lists:
            if item[0]==uucms_no:
                a=str(item)
                z=a.replace("[","")
                y=z.replace("]","")
                x=y.replace("'","")
                an=x.replace(",","        ")
                print("*************************************************************************")
                print("UUCMS          Name           Gender        Course      Sem        Fees")
                print(an)
                print("*************************************************************************")
                #print(item)
                om=False
                break
            elif item[0]!=uucms_no:
                om=True
                pass
        if om==True:
            print("*******************")
            speaker.speak("Record Not Found !")
            print("Record Not Found !")
            print("*******************")  

    elif choice==4:
        f=open("students.csv","r")
        s=f.read()
        b=s.replace("\n","")
        
        all_details_list=b.split(",")
                
        all_lists=[]
        i=0
        l=len(all_details_list)
        while i<l-1:
            j=i+6
            z=all_details_list[i:j]
            all_lists.append(z)
            i=i+6
            f.close()
            # print(all_details_list)
            # print(all_lists)
        speaker.speak("Enter Your U U C M S Number")
        uucms_no=input("Enter UUCMS NO :")
        for item in all_lists:
            if item[0]==uucms_no:
                item.pop(5)
                item.pop(4)
                item.pop(3)
                item.pop(2)
                item.pop(1)
                speaker.speak("Enter Your Name ")
                name=input("Enter Your Name :")
                speaker.speak("Enter Your Gender ")
                gender=input("Enter Your Gender : ")
                speaker.speak("Enter Your Course")
                course=input("Enter Course : ")
                speaker.speak("Enter Your Sem")
                sem=input("Enter Sem :")
                speaker.speak("Enter Your Fees")
                fees=input("Enter Fees : ")
                
                item.insert(1,name)
                item.insert(2,gender)
                item.insert(3,course)
                item.insert(4,sem)
                item.insert(5,fees)
                strs=str(all_lists)
                print(strs)
                omsha=strs.replace("], [",",\n")
                # print(z)
                prefix="[["
                suffix="]]"
                a=omsha.removeprefix(prefix)
                b=a.removesuffix(suffix)
                x=b.replace("[","")

                z=x.replace("],",",\n")
                k=z.replace("'","").strip()
                e=k.replace(", ",",")
                
                f=open("students.csv","w")
                f.write(e)
                f.close()
                print("*************************************************************************")
                speaker.speak("Data Updated Successfully")
                print("Data Updated Successfully !")
                print("*************************************************************************")
                om=False      
                break
            elif item[0]!=uucms_no:
                om=True
                pass
        if om==True:
            print("*******************")
            speaker.speak("Record Not Found !")
            print("Record Not Found !")
            print("*******************")
        
    
    elif choice==5:
        f=open("students.csv","r")
        s=f.read()
        b=s.replace("\n","")
        
        all_details_list=b.split(",")
        
        all_lists=[]
        i=0
        l=len(all_details_list)
        while i<l-1:
            j=i+6
            z=all_details_list[i:j]
            all_lists.append(z)
            i=i+6
            f.close()
            #print(all_details_list)
        speaker.speak("Enter Your U U C M S Number")
        uucms_no=input("Enter UUCMS NO :")
        for item in all_lists:
            if item[0]==uucms_no:
                item.pop(5)
                item.pop(4)
                item.pop(3)
                item.pop(2)
                item.pop(1)
                item.pop(0)
                print("*************************************************************************")
                speaker.speak("Data Deleted Successfully !")
                print("Data Deleted Successfully !")
                print("*************************************************************************")
                strs=str(all_lists)
                #print(strs)
                a=strs.replace(" [], ","")
                x=a.replace(", ",",")
                b=x.replace("[[","")
                c=b.replace("]]","")
                last=c.replace("],[",",\n")
                final=last.replace("'","").strip()
                
                #print(final)
                f=open("students.csv","w")
                f.write(final)
                f.close()
                om=False
                        


                # all_lists.append(item)
                # print(item)
                #print(all_lists)       
                break
            elif item[0]!=uucms_no:
                om=True
                pass
        
        if om==True:
            print("*******************")
            speaker.speak("Record Not Found !")
            print("Record Not Found !")
            print("*******************")
        

        
    
    elif choice==6:
        f=open("students.csv","r")
        s=f.read()
        b=s.replace("\n","")
                
        all_details_list=b.split(",")
                
        all_lists=[]
        i=0
        l=len(all_details_list)
        while i<l-1:
                j=i+6
                z=all_details_list[i:j]
                all_lists.append(z)
                i=i+6
                f.close()
        #print(all_lists)


        print(all_lists)
        print(all_details_list)
        bca=[]
        bba=[]
        ba=[]
        bcom=[]
        bsc=[]
        while True:
            for course in all_lists:
                if course[3]=='BCA':
                    bca.append(course)
            
                elif course[3]=='BBA':
                    bba.append(course)
                    
                elif course[3]=='BA':
                    ba.append(course)
                
                elif course[3]=='B.sc':
                    bcom.append(course)
                
                elif course[3]=='B.com':
                    bsc.append(course)
            break
        print("*************************************************************************")
        print("UUCMS   Name           Gender  Course   Sem     Fees")
        print("*************************************************************************")
        bca=str(bca)
        a=bca.replace("[[","")
        x=a.replace("]]","")
        another=x.replace("], [","\n")
        final=another.replace(",","\t")
        ffinal=final.replace("'","")
        print(ffinal)

        bba=str(bba)
        a=bba.replace("[[","")
        x=a.replace("]]","")
        another=x.replace("], [","\n")
        final=another.replace(",","\t")
        ffinal=final.replace("'","")
        print(ffinal)

        ba=str(ba)
        a=ba.replace("[[","")
        x=a.replace("]]","")
        another=x.replace("], [","\n")
        final=another.replace(",","\t")
        ffinal=final.replace("'","")
        print(ffinal)

        bcom=str(bcom)
        a=bcom.replace("[[","")
        x=a.replace("]]","")
        another=x.replace("], [","\n")
        final=another.replace(",","\t")
        ffinal=final.replace("'","")
        print(ffinal)

        bsc=str(bsc)
        a=bsc.replace("[[","")
        x=a.replace("]]","")
        another=x.replace("], [","\n")
        final=another.replace(",","\t")
        ffinal=final.replace("'","")
        print(ffinal)
    
    elif choice==7:
        f=open("students.csv","r")
        s=f.read()
        b=s.replace("\n","")
                
        all_details_list=b.split(",")
                
        all_lists=[]
        i=0
        l=len(all_details_list)
        while i<l-1:
                j=i+6
                z=all_details_list[i:j]
                all_lists.append(z)
                i=i+6
                f.close()
        #print(all_lists)
        #print(all_details_list)


        bca=[]
        bba=[]
        ba=[]
        bcom=[]
        bsc=[]
        while True:
            for course in all_lists:
                if course[3]=='BCA':
                    bca.append(course)
            
                elif course[3]=='BBA':
                    bba.append(course)
                    
                elif course[3]=='BA':
                    ba.append(course)
                
                elif course[3]=='B.sc':
                    bcom.append(course)
                
                elif course[3]=='B.com':
                    bsc.append(course)
            break

        
        
        bca_count=all_details_list.count('BCA')
        bba_count=all_details_list.count('BBA')
        ba_count=all_details_list.count('BA')
        bsc_count=all_details_list.count('B.sc')
        bcom_count=all_details_list.count('B.com')
        print("*************************************************************************")
        print(f"BCA Course Students : {bca_count}")
        print(f"BBA Course Students: {bba_count}")
        print(f"BA Course Students: {ba_count}")
        print(f"B.sc Course Students: {bsc_count}")
        print(f"B.com : {bcom_count}")
        print("*************************************************************************")
    elif choice==8:
        speaker.speak("Thank You for Using our Services !")
        print("***************************Thank You For Using Our Services*********************************** ")
        break

        