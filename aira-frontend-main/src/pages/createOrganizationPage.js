import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Card, CardContent, TextField, Button, Typography } from '@mui/material';
import { createOrganization } from '../services/api/core';

const CreateOrganizationPage = () => {
    const [name, setName] = useState('');
    const [error, setError] = useState('');
    const navigate = useNavigate();

    const handleCreate = async () => {
        try {
            await createOrganization({ name });
            setError('');
            navigate('/workspace');
        } catch (err) {
            setError('Failed to create organization.');
        }
    };

    return (
        <Card>
            <CardContent>
                <Typography variant="h5" component="div">
                    Create Organization
                </Typography>
                <TextField
                    label="Organization Name"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    fullWidth
                    margin="normal"
                />
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

export default CreateOrganizationPage;