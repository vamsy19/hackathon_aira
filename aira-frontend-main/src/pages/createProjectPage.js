import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Card, CardContent, TextField, Button, Typography, Grid, MenuItem } from '@mui/material';
import { createProject, fetchOrganizations } from '../services/api/core';

const CreateProjectPage = () => {
    const [name, setName] = useState('');
    const [description, setDescription] = useState('');
    const [organization, setOrganization] = useState('');
    const [startDate, setStartDate] = useState('');
    const [endDate, setEndDate] = useState('');
    const [organizations, setOrganizations] = useState([]);
    const [error, setError] = useState('');
    const navigate = useNavigate();

    useEffect(() => {
        const loadOrganizations = async () => {
            try {
                const data = await fetchOrganizations();
                setOrganizations(data);
            } catch (err) {
                setError('Failed to fetch organizations.');
            }
        };
        loadOrganizations();
    }, []);

    const handleCreate = async () => {
        try {
            await createProject({ name, description, organization, start_date: startDate, end_date: endDate });
            setError('');
            navigate('/workspace');
        } catch (err) {
            setError('Failed to create project.');
        }
    };

    return (
        <Card>
            <CardContent>
                <Typography variant="h5" component="div">
                    Create Project
                </Typography>
                <Grid container spacing={2}>
                    <Grid item xs={12}>
                        <TextField
                            label="Project Name"
                            value={name}
                            onChange={(e) => setName(e.target.value)}
                            fullWidth
                            margin="normal"
                        />
                    </Grid>
                    <Grid item xs={12}>
                        <TextField
                            label="Description"
                            value={description}
                            onChange={(e) => setDescription(e.target.value)}
                            fullWidth
                            margin="normal"
                        />
                    </Grid>
                    <Grid item xs={12}>
                        <TextField
                            select
                            label="Organization"
                            value={organization}
                            onChange={(e) => setOrganization(e.target.value)}
                            fullWidth
                            margin="normal"
                        >
                            {organizations.map((org) => (
                                <MenuItem key={org.id} value={org.id}>
                                    {org.name}
                                </MenuItem>
                            ))}
                        </TextField>
                    </Grid>
                    <Grid item xs={6}>
                        <TextField
                            label="Start Date"
                            type="date"
                            value={startDate}
                            onChange={(e) => setStartDate(e.target.value)}
                            fullWidth
                            margin="normal"
                            InputLabelProps={{
                                shrink: true,
                            }}
                        />
                    </Grid>
                    <Grid item xs={6}>
                        <TextField
                            label="End Date"
                            type="date"
                            value={endDate}
                            onChange={(e) => setEndDate(e.target.value)}
                            fullWidth
                            margin="normal"
                            InputLabelProps={{
                                shrink: true,
                            }}
                        />
                    </Grid>
                </Grid>
                {error && (
                    <Typography color="error" variant="body2">
                        {error}
                    </Typography>
                )}
                <Button variant="contained" color="primary" onClick={handleCreate}>
                    Create
                </Button>
            </CardContent>
        </Card>
    );
};

export default CreateProjectPage;