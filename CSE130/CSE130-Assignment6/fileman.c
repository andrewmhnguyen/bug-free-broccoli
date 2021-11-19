/*********************************************************************
 *
 * Copyright (C) 2020-2021 David C. Harrison. All right reserved.
 *
 * You may not use, distribute, publish, or modify this code without 
 * the express written permission of the copyright holder.
 *
 ***********************************************************************/

#include "fileman.h"
#include<sys/types.h>
#include<sys/stat.h>
#include <fcntl.h>  
#include <unistd.h>

/*
 * You need to implement this function, see fileman.h for details 
 */
int fileman_read(char *fname, size_t foffset, char *buf, size_t boffset, size_t size) {
	int fd = open(fname, O_RDONLY);
	if (fd == -1){
		return -1;
	}
	lseek(fd, foffset, SEEK_SET);
	int off = read(fd, buf+boffset, size);
	close(fd);
	return off;
}

/*
 * You need to implement this function, see fileman.h for details 
 */
int fileman_write(char *fname, size_t foffset, char *buf, size_t boffset, size_t size) {
	mode_t mode = S_IRUSR | S_IWUSR | S_IRGRP | S_IROTH;
	int fd = open(fname, O_WRONLY|O_CREAT|O_TRUNC|O_EXCL, mode);
	if (fd == -1){
		return -1;
	}
	lseek(fd, foffset, SEEK_SET);
	int off = write(fd, buf+boffset, size);
	close(fd);
	return off;
}

/*
 * You need to implement this function, see fileman.h for details 
 */
int fileman_append(char *fname, char *buf, size_t size) {
	return -1;
}

/*
 * You need to implement this function, see fileman.h for details 
 */
int fileman_copy(char *fsrc, char *fdest) {
	// Remove, only here to fail code warning test
	return -1;
}

/*
 * You need to implement this function, see fileman.h for details 
 */
void fileman_dir(int fd, char *dname) {
}

/*
 * You need to implement this function, see fileman.h for details 
 */
void fileman_tree(int fd, char *dname) {
}
