import React, { Component } from "react";
import Button from "@material-ui/core/Button";
import Grid from "@material-ui/core/Grid";
import Typography from "@material-ui/core/Typography";
import axios from 'axios';
import { withStyles } from '@material-ui/core/styles';
import {
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  TablePagination,
} from '@mui/material';


export default class GetQueries extends Component {
  logged_in = false;

  constructor(props) {
    super(props);
    this.state = {
      songDescription: '',
      myList: [{'song':'none'}],
      isParagraphVisible: false,
      page: 0,
      rowsPerPage: 5
    };

    this.getUserQueries = this.getUserQueries.bind(this);
    this.handleChangePage = this.handleChangePage.bind(this);
    this.handleChangeRowsPerPage = this.handleChangeRowsPerPage.bind(this);
  }

  // Function to toggle the visibility of the paragraph
  toggleParagraph = () => {
    this.setState({ isParagraphVisible: !this.state.isParagraphVisible });
  };

  getUserQueries= async () => {
      const instance = axios.create({
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });
      
      // Now use 'instance' for your requests instead of 'axios'
      instance.get(`http://localhost/api/get-user-queries/`).then(response => {
          // Handle the response
          const data = response.data
          let l = [];
          for (let i = 0; i < data['query_list'].length; i++) {
            l.push(data['query_list'][i])
        }
        this.setState({
            myList: l,
        });}).catch(error => {
            console.error('Get song failed:', error.message);
        });
        this.toggleParagraph();

  }

  handleChangePage(event, newPage) {
    this.setState(
      {
        page: newPage
      }
    )
  };

  handleChangeRowsPerPage(event){
    this.setState(
      {
        page: 0,
      rowsPerPage: parseInt(event.target.value, 10)
      }
    )
  };

  render() {
    const { username } = this.props;
    const styles = {
      boldCenteredText: {
        fontWeight: 'bold',
        textAlign: 'center',
      },
      boldHeadCenteredText: {
        fontWeight: 'bold',
        textAlign: 'center',
        fontSize: '20px',
      },
    };

    const CustomTableCell = withStyles(styles)(({ classes, children }) => (
      <TableCell className={classes.boldCenteredText}>
        {children}
      </TableCell>
    ));
    const CustomTableHead = withStyles(styles)(({ classes, children }) => (
      <TableCell className={classes.boldHeadCenteredText}>
        {children}
      </TableCell>
    ));
    return (
      <Grid  container spacing={1} >
      <div style={{ height: '100vh',width: '100vw', overflow: 'auto' }}>
        
        <Grid item xs={12} align="center">
          <Typography component="h4" variant="h4">
            Welcome {username} 
          </Typography>
        </Grid>
        <div style={{ margin: '16px' }} />
        <Grid item xs={12} align="center">
          <Button
            color="primary"
            variant="contained"
            onClick={this.getUserQueries}
          >
            Get History
          </Button>
        </Grid>
        <div style={{ margin: '16px' }} />
        <Grid  item xs={12} align="center">
        {this.state.isParagraphVisible && (
          
          
        <TableContainer component={Paper}>
          <Table>
            <TableHead>
              <TableRow>
                <CustomTableHead>Name</CustomTableHead>
                {/* Add more TableCell components for additional columns */}
              </TableRow>
            </TableHead>
            <TableBody>
              {(this.state.rowsPerPage > 0
                ? this.state.myList.slice(this.state.page * this.state.rowsPerPage, this.state.page * this.state.rowsPerPage + this.state.rowsPerPage)
                : this.state.myList
              ).map((row) => (
                <TableRow key={row.description}>
                  <CustomTableCell>{row.description}</CustomTableCell>
                  {/* Add more TableCell components for additional columns */}
                </TableRow>
              ))}
            </TableBody>
          </Table>
          <TablePagination
            rowsPerPageOptions={[5, 10, 25]}
            component="div"
            count={this.state.myList.length}
            rowsPerPage={this.state.rowsPerPage}
            page={this.state.page}
            onPageChange={this.handleChangePage}
            onRowsPerPageChange={this.handleChangeRowsPerPage}
          />
        </TableContainer>)}
          </Grid>
        </div>
        </Grid>);
    }
  }




















